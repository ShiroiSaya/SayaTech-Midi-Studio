from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class TrackInfo:
    index: int
    name: str
    note_count: int
    min_note: Optional[int]
    max_note: Optional[int]
    channels: List[int] = field(default_factory=list)
    has_pedal: bool = False
    looks_like_drum: bool = False


@dataclass(slots=True)
class NoteSpan:
    track_index: int
    start_sec: float
    end_sec: float
    midi_note: int
    velocity: int


@dataclass(slots=True)
class PedalEvent:
    track_index: int
    time_sec: float
    is_down: bool


@dataclass(slots=True)
class TimelineOverview:
    duration_sec: float
    bars: List[float]
    active_sections: List[bool]


@dataclass(slots=True)
class MidiAnalysisResult:
    file_path: str
    track_infos: List[TrackInfo]
    notes: List[NoteSpan]
    pedal_events: List[PedalEvent]
    timeline: TimelineOverview
    duration_sec: float
    min_note: int
    max_note: int
    primary_bpm: float = 120.0
    has_tempo_changes: bool = False

    @property
    def recommended_track_indexes(self) -> List[int]:
        note_tracks = [t.index for t in self.track_infos if t.note_count > 0 and not t.looks_like_drum]
        if len(note_tracks) <= 1:
            return note_tracks
        counts = [t.note_count for t in self.track_infos if t.note_count > 0 and not t.looks_like_drum]
        top = max(counts) if counts else 0
        threshold = max(1, int(top * 0.08))
        return [t.index for t in self.track_infos if t.note_count >= threshold and not t.looks_like_drum]

    @property
    def recommended_drum_indexes(self) -> List[int]:
        drum_tracks = [t.index for t in self.track_infos if t.note_count > 0 and t.looks_like_drum]
        return drum_tracks or [t.index for t in self.track_infos if t.note_count > 0]


@dataclass(slots=True)
class DrumPlanReport:
    selected_mode: str
    total_source_hits: int
    total_mapped_hits: int
    note_counter: List[tuple[int, int]] = field(default_factory=list)
    mapped_counter: List[tuple[str, int]] = field(default_factory=list)
    fallback_counter: List[tuple[str, int]] = field(default_factory=list)
    ignored_counter: List[tuple[str, int]] = field(default_factory=list)
    preview_rows: List[tuple[str, int, str, str]] = field(default_factory=list)
