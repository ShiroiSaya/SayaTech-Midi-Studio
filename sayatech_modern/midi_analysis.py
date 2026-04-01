from __future__ import annotations

import os
from collections import defaultdict
from typing import DefaultDict, Iterable, List, Tuple

import mido

from .models import MidiAnalysisResult, NoteSpan, PedalEvent, TimelineOverview, TrackInfo

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_to_note_name(note: int) -> str:
    return f"{NOTE_NAMES[note % 12]}{note // 12 - 1}"


def extract_track_name(track, idx: int) -> str:
    for msg in track:
        if msg.type == "track_name":
            name = str(getattr(msg, "name", "")).strip()
            if name:
                return name
    return f"Track {idx + 1}"


def track_looks_like_drum(track, idx: int) -> bool:
    name = extract_track_name(track, idx).lower()
    if any(tag in name for tag in ("drum", "kit", "perc", "percussion", "鼓")):
        return True
    note_count = 0
    channel9_count = 0
    for msg in track:
        if msg.type in ("note_on", "note_off"):
            note_count += 1
            if getattr(msg, "channel", -1) == 9:
                channel9_count += 1
    return note_count > 0 and channel9_count / max(1, note_count) >= 0.5


def _build_timeline(notes: Iterable[NoteSpan], duration: float, bins: int = 96) -> TimelineOverview:
    notes = list(notes)
    bars = [0.0 for _ in range(max(1, bins))]
    active_sections = [False for _ in range(max(1, bins))]
    if duration > 0:
        bin_width = duration / len(bars)
        for note in notes:
            start_idx = min(len(bars) - 1, int(note.start_sec / max(0.001, bin_width)))
            end_idx = min(len(bars) - 1, int(note.end_sec / max(0.001, bin_width)))
            for idx in range(start_idx, end_idx + 1):
                bars[idx] += note.velocity / 127.0
                active_sections[idx] = True
        peak = max(bars) if max(bars, default=0.0) > 0 else 1.0
        bars = [v / peak for v in bars]
    return TimelineOverview(duration_sec=duration, bars=bars, active_sections=active_sections)


def analyze_midi(file_path: str, bins: int = 96, pedal_threshold: int = 64) -> MidiAnalysisResult:
    mid = mido.MidiFile(file_path)

    track_infos: List[TrackInfo] = []
    for idx, track in enumerate(mid.tracks):
        note_count = 0
        min_note = None
        max_note = None
        channels = set()
        has_pedal = False
        looks_like_drum = track_looks_like_drum(track, idx)
        for msg in track:
            if msg.type == "control_change" and getattr(msg, "control", -1) == 64:
                has_pedal = True
            if msg.type in ("note_on", "note_off"):
                channels.add(getattr(msg, "channel", 0) + 1)
                if msg.type == "note_on" and getattr(msg, "velocity", 0) > 0:
                    note_count += 1
                    note = int(msg.note)
                    min_note = note if min_note is None else min(min_note, note)
                    max_note = note if max_note is None else max(max_note, note)
        track_infos.append(
            TrackInfo(
                index=idx,
                name=extract_track_name(track, idx),
                note_count=note_count,
                min_note=min_note,
                max_note=max_note,
                channels=sorted(channels),
                has_pedal=has_pedal,
                looks_like_drum=looks_like_drum,
            )
        )

    events: List[Tuple[int, int, int, object]] = []
    for track_idx, track in enumerate(mid.tracks):
        abs_tick = 0
        order = 0
        for msg in track:
            abs_tick += msg.time
            events.append((abs_tick, order, track_idx, msg))
            order += 1
    events.sort(key=lambda x: (x[0], x[1], x[2]))

    tempo = 500000
    first_tempo = 500000
    tempo_change_count = 0
    last_tick = 0
    abs_sec = 0.0
    active: DefaultDict[Tuple[int, int, int], List[Tuple[float, int]]] = defaultdict(list)
    notes: List[NoteSpan] = []
    pedal_events: List[PedalEvent] = []

    for abs_tick, _order, track_idx, msg in events:
        delta_tick = abs_tick - last_tick
        if delta_tick:
            abs_sec += mido.tick2second(delta_tick, mid.ticks_per_beat, tempo)
            last_tick = abs_tick

        if msg.type == "set_tempo":
            tempo = msg.tempo
            tempo_change_count += 1
            if tempo_change_count == 1:
                first_tempo = msg.tempo
            continue
        if msg.type == "control_change" and getattr(msg, "control", -1) == 64:
            pedal_events.append(
                PedalEvent(
                    track_index=track_idx,
                    time_sec=abs_sec,
                    is_down=int(getattr(msg, "value", 0)) >= pedal_threshold,
                )
            )
            continue
        if msg.type == "note_on" and getattr(msg, "velocity", 0) > 0:
            active[(track_idx, getattr(msg, "channel", 0), int(msg.note))].append((abs_sec, int(getattr(msg, "velocity", 0))))
        elif msg.type == "note_off" or (msg.type == "note_on" and getattr(msg, "velocity", 0) == 0):
            key = (track_idx, getattr(msg, "channel", 0), int(msg.note))
            if active.get(key):
                st_sec, velocity = active[key].pop(0)
                notes.append(
                    NoteSpan(
                        track_index=track_idx,
                        start_sec=st_sec,
                        end_sec=max(abs_sec, st_sec + 0.04),
                        midi_note=int(msg.note),
                        velocity=velocity,
                    )
                )

    for (track_idx, _channel, note), stack in active.items():
        for st_sec, velocity in stack:
            notes.append(
                NoteSpan(
                    track_index=track_idx,
                    start_sec=st_sec,
                    end_sec=st_sec + 0.2,
                    midi_note=int(note),
                    velocity=velocity,
                )
            )

    notes.sort(key=lambda n: (n.start_sec, n.track_index, n.midi_note))
    duration = max((n.end_sec for n in notes), default=0.0)
    min_note = min((n.midi_note for n in notes), default=48)
    max_note = max((n.midi_note for n in notes), default=84)
    timeline = _build_timeline(notes, duration, bins=bins)

    return MidiAnalysisResult(
        file_path=os.path.abspath(file_path),
        track_infos=track_infos,
        notes=notes,
        pedal_events=pedal_events,
        timeline=timeline,
        duration_sec=duration,
        min_note=min_note,
        max_note=max_note,
        primary_bpm=round(mido.tempo2bpm(first_tempo), 1),
        has_tempo_changes=tempo_change_count > 1,
    )


def filter_analysis(analysis: MidiAnalysisResult, selected_track_indexes: Iterable[int], *, bins: int = 96) -> MidiAnalysisResult:
    selected_set = {int(idx) for idx in selected_track_indexes}
    filtered_notes = [note for note in analysis.notes if note.track_index in selected_set] if selected_set else list(analysis.notes)
    min_note = min((n.midi_note for n in filtered_notes), default=analysis.min_note)
    max_note = max((n.midi_note for n in filtered_notes), default=analysis.max_note)
    timeline = _build_timeline(filtered_notes, analysis.duration_sec, bins=bins)
    filtered_tracks = [track for track in analysis.track_infos if track.index in selected_set] if selected_set else list(analysis.track_infos)
    filtered_pedals = [event for event in analysis.pedal_events if event.track_index in selected_set] if selected_set else list(analysis.pedal_events)
    return MidiAnalysisResult(
        file_path=analysis.file_path,
        track_infos=filtered_tracks,
        notes=filtered_notes,
        pedal_events=filtered_pedals,
        timeline=timeline,
        duration_sec=analysis.duration_sec,
        min_note=min_note,
        max_note=max_note,
        primary_bpm=analysis.primary_bpm,
        has_tempo_changes=analysis.has_tempo_changes,
    )
