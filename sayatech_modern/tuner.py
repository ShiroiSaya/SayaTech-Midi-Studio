from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .backend import ModernPianoBackend
from .config_io import midi_to_note_name
from .models import MidiAnalysisResult, NoteSpan

PREVIEW_LABELS: List[Tuple[str, str]] = [
    ("LEFTMOST_NOTE", "基础窗口起点"),
    ("VISIBLE_OCTAVES", "窗口八度数"),
    ("UNLOCKED_MIN_NOTE", "可弹最低音"),
    ("UNLOCKED_MAX_NOTE", "可弹最高音"),
    ("AUTO_SHIFT_FROM_RANGE", "按音域自动判断右移窗口"),
    ("USE_SHIFT_OCTAVE", "启用右移窗口"),
    ("LOOKAHEAD_NOTES", "预读音符数"),
    ("SWITCH_MARGIN", "切换保守度"),
    ("MIN_NOTES_BETWEEN_SWITCHES", "切换冷却音符数"),
    ("SHIFT_WEIGHT", "右移窗口偏好"),
    ("BAR_AWARE_TRANSPOSE", "启用局部移八度"),
    ("BAR_TRANSPOSE_SCOPE", "局部移八度范围"),
    ("MELODY_KEEP_TOP", "旋律保留层数"),
    ("SHIFT_HOLD_BASS", "保留低音层"),
    ("SHIFT_HOLD_MAX_NOTE", "低音保留上限"),
    ("MIN_NOTE_LEN", "最短按键时长"),
    ("OCTAVE_AVOID_COLLISION", "启用防撞"),
    ("OCTAVE_PREVIEW_NEIGHBORS", "邻近预览数量"),
    ("RETRIGGER_PRIORITY", "重叠音释放策略"),
]


def _round_left_to_c(note: int) -> int:
    return max(12, (note // 12) * 12)


def _safe_int(current_config: Dict[str, Any], key: str, default: int) -> int:
    try:
        return int(current_config.get(key, default))
    except Exception:
        return default


def _safe_float(current_config: Dict[str, Any], key: str, default: float) -> float:
    try:
        return float(current_config.get(key, default))
    except Exception:
        return default


def _safe_bool(current_config: Dict[str, Any], key: str, default: bool) -> bool:
    value = current_config.get(key, default)
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _group_notes(notes: List[NoteSpan], threshold: float) -> List[List[NoteSpan]]:
    groups: List[List[NoteSpan]] = []
    if not notes:
        return groups
    ordered = sorted(notes, key=lambda n: (n.start_sec, n.midi_note))
    i = 0
    while i < len(ordered):
        base = ordered[i]
        group = [base]
        j = i + 1
        while j < len(ordered) and ordered[j].start_sec - base.start_sec <= threshold:
            group.append(ordered[j])
            j += 1
        groups.append(group)
        i = j
    return groups


def _feature_summary(analysis: MidiAnalysisResult, threshold: float) -> Dict[str, Any]:
    notes = analysis.notes
    groups = _group_notes(notes, threshold)
    note_values = [n.midi_note for n in notes] or [60]
    durations = [max(0.0, n.end_sec - n.start_sec) for n in notes] or [0.1]
    melody = [max(group, key=lambda n: n.midi_note).midi_note for group in groups if group]
    jumps = [abs(melody[i] - melody[i - 1]) for i in range(1, len(melody))]
    short_008 = sum(1 for d in durations if d <= 0.08)
    short_006 = sum(1 for d in durations if d <= 0.06)
    return {
        "note_count": len(notes),
        "min_note": min(note_values),
        "max_note": max(note_values),
        "avg_chord": sum(len(g) for g in groups) / max(1, len(groups)),
        "max_chord": max((len(g) for g in groups), default=1),
        "high_ratio": sum(1 for n in note_values if n >= 84) / max(1, len(note_values)),
        "low_ratio": sum(1 for n in note_values if n <= 59) / max(1, len(note_values)),
        "avg_jump": sum(jumps) / max(1, len(jumps)) if jumps else 0.0,
        "max_jump": max(jumps) if jumps else 0,
        "avg_duration": sum(durations) / max(1, len(durations)),
        "short_ratio_008": short_008 / max(1, len(durations)),
        "short_ratio_006": short_006 / max(1, len(durations)),
        "groups": groups,
    }


class MultiCandidateTuner:
    def __init__(self, analysis: MidiAnalysisResult, current_config: Dict[str, Any], playable_range: Tuple[int, int]):
        self.analysis = analysis
        self.current_config = dict(current_config)
        user_min, user_max = playable_range
        if user_min > user_max:
            user_min, user_max = user_max, user_min
        self.user_min = user_min
        self.user_max = user_max
        self.threshold = _safe_float(current_config, "CHORD_SPLIT_THRESHOLD", 0.05)
        self.feat = _feature_summary(analysis, self.threshold)
        self.groups: List[List[NoteSpan]] = self.feat["groups"]
        self.backend = ModernPianoBackend()
        self.backend.update_config(self.current_config)
        self.group_note_prefix: List[int] = [0]
        running = 0
        for group in self.groups:
            self.group_note_prefix.append(running)
            running += len(group)
        self.total_group_count = len(self.groups)
        self.total_note_count = running
        self.probe_group_indexes = self._build_probe_group_indexes()
        self.full_eval_group_indexes = self._build_full_eval_group_indexes()


    def _range_fits_window(self, leftmost: int, visible_octaves: int) -> bool:
        right_edge = int(leftmost) + max(1, int(visible_octaves)) * 12 - 1
        return self.user_min >= int(leftmost) and self.user_max <= right_edge

    def _is_fixed_window_candidate(self, merged: Dict[str, Any]) -> bool:
        return bool(merged.get("AUTO_SHIFT_FROM_RANGE", True)) and self._range_fits_window(int(merged.get("LEFTMOST_NOTE", self.user_min)), int(merged.get("VISIBLE_OCTAVES", 3)))


    def _build_full_eval_group_indexes(self) -> List[int]:
        total = len(self.groups)
        if total <= 240:
            return list(range(total))
        target = 180
        if total >= 600 or self.feat["note_count"] >= 4500:
            target = 144
        if total >= 1200 or self.feat["note_count"] >= 9000:
            target = 120
        return self._build_group_sample(target=target, head_tail=18, top_weighted=36)

    def _build_group_sample(self, *, target: int, head_tail: int, top_weighted: int) -> List[int]:
        total = len(self.groups)
        if total <= target:
            return list(range(total))

        important: set[int] = set()
        head = min(head_tail, total)
        tail = min(head_tail, total)
        important.update(range(head))
        important.update(range(max(0, total - tail), total))

        weighted: List[Tuple[float, int]] = []
        for idx, group in enumerate(self.groups):
            size = float(len(group))
            min_note = min(n.midi_note for n in group)
            max_note = max(n.midi_note for n in group)
            pressure = sum(1 for n in group if n.midi_note < self.user_min or n.midi_note > self.user_max)
            edge_penalty = max(0, max_note - self.user_max) + max(0, self.user_min - min_note)
            weight = pressure * 4.0 + size * 1.6 + edge_penalty * 0.35
            weighted.append((weight, idx))
        weighted.sort(reverse=True)
        for _weight, idx in weighted[: min(top_weighted, total)]:
            important.add(idx)

        sampled = set(important)
        remaining = max(0, target - len(sampled))
        if remaining > 0:
            stride = max(1, total // remaining)
            sampled.update(range(0, total, stride))
            sampled.add(total - 1)

        result = sorted(sampled)
        if len(result) <= target:
            return result

        pinned = sorted(important)
        rest = [idx for idx in result if idx not in important]
        keep_rest = max(0, target - len(pinned))
        if keep_rest <= 0:
            return pinned[:target]
        if len(rest) <= keep_rest:
            return sorted(pinned + rest)
        trimmed: List[int] = []
        step = (len(rest) - 1) / max(1, keep_rest - 1) if keep_rest > 1 else 0.0
        for i in range(keep_rest):
            trimmed.append(rest[round(i * step)] if rest else 0)
        return sorted(set(pinned + trimmed))

    def _build_probe_group_indexes(self) -> List[int]:
        total = len(self.groups)
        if total <= 96:
            return list(range(total))
        target = 72
        if total >= 600 or self.feat["note_count"] >= 4500:
            target = 60
        if total >= 1200 or self.feat["note_count"] >= 9000:
            target = 48
        return self._build_group_sample(target=target, head_tail=12, top_weighted=24)

    def _score_group_indexes(
        self,
        merged: Dict[str, Any],
        group_indexes: List[int],
        *,
        stop_above: Optional[float] = None,
    ) -> Tuple[float, Dict[str, Any]]:
        self.backend.update_config(merged)
        if not self.groups or not group_indexes:
            return 999999.0, {
                "lost": 0,
                "melody_loss": 0,
                "harsh_fold": 0,
                "switch_need": 0,
                "collision_penalty": 0.0,
                "duration_penalty": 0.0,
                "low_layer_bonus": 0.0,
                "sampled_groups": 0,
            }

        allowed_offsets = self.backend._allowed_offsets()
        current_offset = 0 if 0 in allowed_offsets else allowed_offsets[0]
        last_switch_note_index = 0
        prev_melody_note: Optional[int] = None

        lost = 0
        melody_loss = 0
        harsh_fold = 0.0
        collision_penalty = 0.0
        fold_penalty = 0.0
        switch_need = 0
        duration_penalty = 0.0
        low_layer_bonus = 0.0
        upper_switches = 0

        sampled_ratio = len(group_indexes) / max(1, len(self.groups))
        for group_index in group_indexes:
            group = self.groups[group_index]
            notes_seen_before = self.group_note_prefix[group_index]
            notes_since_switch = max(0, notes_seen_before - last_switch_note_index)
            target_offset = self.backend._choose_best_offset(
                self.groups,
                group_index,
                current_offset,
                prev_melody_note,
                notes_since_switch=notes_since_switch,
            )
            if target_offset != current_offset:
                switch_need += 1
                if target_offset > current_offset:
                    upper_switches += 1
                current_offset = target_offset
                last_switch_note_index = notes_seen_before

            ordered_group, melody_note, _melody_rank_map, low_rank_map = self.backend._ordered_group_notes(group, prev_melody_note)
            used_key_indexes: set[int] = set()
            mapped_melody: Optional[int] = None
            group_low_bonus = 0.0
            for note in ordered_group:
                prev_hint = prev_melody_note if note is melody_note else None
                mapped_note, fold_distance, jump_excess = self.backend._map_note_with_meta(note.midi_note, current_offset, prev_hint)
                if mapped_note is None:
                    lost += 1
                    continue
                if note is melody_note:
                    mapped_melody = mapped_note
                key_index = mapped_note - self.backend._window_left(current_offset)
                if self.backend.octave_avoid_collision and key_index in used_key_indexes:
                    collision_penalty += 1.0
                used_key_indexes.add(key_index)
                fold_penalty += fold_distance
                harsh_fold += jump_excess
                note_duration = max(0.0, note.end_sec - note.start_sec)
                if note_duration < self.backend.min_note_len:
                    duration_penalty += (self.backend.min_note_len - note_duration) * 18.0
                chord_rank = low_rank_map.get(id(note), 0)
                if self.backend.shift_hold_bass and chord_rank <= self.backend.shift_hold_max_chord_rank and note.midi_note <= self.backend.shift_hold_max_note:
                    group_low_bonus += 0.20 if target_offset > 0 else 0.08
            if mapped_melody is None:
                melody_loss += 1
            else:
                prev_melody_note = mapped_melody
            if target_offset > 0:
                low_layer_bonus += group_low_bonus

            if stop_above is not None:
                partial = (
                    lost * 150.0
                    + melody_loss * 30.0
                    + fold_penalty * (7.0 + float(merged["OCTAVE_FOLD_WEIGHT"]) * 4.0)
                    + harsh_fold * 0.85
                    + collision_penalty * 3.6
                    + switch_need * max(0.35, float(merged["SHIFT_WEIGHT"]) - 0.95)
                    + duration_penalty
                    - low_layer_bonus
                )
                relaxed_cutoff = stop_above * (1.18 if sampled_ratio < 0.999 else 1.04) + 4.0
                if partial > relaxed_cutoff:
                    break

        if self.backend.min_note_len < 0.055:
            duration_penalty += (0.055 - self.backend.min_note_len) * 55.0

        fixed_window = self._is_fixed_window_candidate(merged)
        if fixed_window and not bool(merged.get("USE_SHIFT_OCTAVE", True)):
            low_layer_bonus += 1.2
            switch_need = 0

        score = (
            lost * 150.0
            + melody_loss * 30.0
            + fold_penalty * (7.0 + float(merged["OCTAVE_FOLD_WEIGHT"]) * 4.0)
            + harsh_fold * 0.85
            + collision_penalty * 3.6
            + switch_need * max(0.35, float(merged["SHIFT_WEIGHT"]) - 0.95)
            + duration_penalty
            - low_layer_bonus
        )
        return score, {
            "lost": int(lost),
            "melody_loss": int(melody_loss),
            "harsh_fold": round(harsh_fold, 2),
            "switch_need": int(switch_need),
            "upper_switches": int(upper_switches),
            "collision_penalty": round(collision_penalty, 2),
            "duration_penalty": round(duration_penalty, 2),
            "low_layer_bonus": round(low_layer_bonus, 2),
            "sampled_groups": len(group_indexes),
            "fixed_window_mode": fixed_window,
        }

    def _normalize_candidate(self, cfg: Dict[str, Any]) -> Dict[str, Any]:
        merged = dict(self.current_config)
        merged.update(cfg)
        merged["UNLOCKED_MIN_NOTE"] = self.user_min
        merged["UNLOCKED_MAX_NOTE"] = self.user_max
        visible_octaves = max(1, int(merged.get("VISIBLE_OCTAVES", 3)))
        merged["VISIBLE_OCTAVES"] = visible_octaves
        leftmost = int(merged.get("LEFTMOST_NOTE", self.user_min))
        leftmost = max(self.user_min, _round_left_to_c(leftmost))
        max_leftmost = max(self.user_min, self.user_max - visible_octaves * 12 + 1)
        merged["LEFTMOST_NOTE"] = min(leftmost, max_leftmost)
        merged["AUTO_SHIFT_FROM_RANGE"] = bool(merged.get("AUTO_SHIFT_FROM_RANGE", True))
        merged["USE_SHIFT_OCTAVE"] = bool(merged.get("USE_SHIFT_OCTAVE", True))
        right_edge = int(merged["LEFTMOST_NOTE"]) + visible_octaves * 12 - 1
        fixed_window = bool(merged["AUTO_SHIFT_FROM_RANGE"]) and self.user_min >= int(merged["LEFTMOST_NOTE"]) and self.user_max <= right_edge
        if fixed_window:
            merged["USE_SHIFT_OCTAVE"] = False
            merged["SWITCH_MARGIN"] = 0
            merged["MIN_NOTES_BETWEEN_SWITCHES"] = max(0, int(merged.get("MIN_NOTES_BETWEEN_SWITCHES", 0)))
            merged["SHIFT_WEIGHT"] = max(0.1, min(float(merged.get("SHIFT_WEIGHT", 1.0)), 1.0))
        merged["OCTAVE_PREVIEW_NEIGHBORS"] = max(0, int(merged.get("OCTAVE_PREVIEW_NEIGHBORS", 0)))
        merged["SWITCH_MARGIN"] = max(0, int(merged.get("SWITCH_MARGIN", 0)))
        merged["MIN_NOTES_BETWEEN_SWITCHES"] = max(0, int(merged.get("MIN_NOTES_BETWEEN_SWITCHES", 0)))
        merged["LOOKAHEAD_NOTES"] = max(8, int(merged.get("LOOKAHEAD_NOTES", 24)))
        merged["MIN_NOTE_LEN"] = max(0.03, float(merged.get("MIN_NOTE_LEN", 0.1)))
        merged["SHIFT_WEIGHT"] = max(0.1, float(merged.get("SHIFT_WEIGHT", 1.6)))
        merged["OCTAVE_FOLD_WEIGHT"] = max(0.2, float(merged.get("OCTAVE_FOLD_WEIGHT", 0.55)))
        merged["OCTAVE_LOOKAHEAD"] = max(int(merged.get("OCTAVE_LOOKAHEAD", 0)), int(merged["LOOKAHEAD_NOTES"]))
        return merged

    def build_seed(self) -> Dict[str, Any]:
        note_span = self.feat["max_note"] - self.feat["min_note"] + 1
        playable_span = self.user_max - self.user_min + 1
        current_leftmost = _safe_int(self.current_config, "LEFTMOST_NOTE", self.user_min)
        visible_octaves = _safe_int(self.current_config, "VISIBLE_OCTAVES", 3)
        if playable_span < visible_octaves * 12:
            visible_octaves = max(1, min(visible_octaves, max(1, playable_span // 12)))
        window_size = max(12, visible_octaves * 12)
        max_leftmost = max(self.user_min, self.user_max - window_size + 1)
        leftmost = min(max(_round_left_to_c(current_leftmost), self.user_min), max_leftmost)

        if note_span <= playable_span:
            lookahead = 20 if note_span <= 24 else 24
            switch_margin = 0
            shift_weight = 1.0
        elif note_span <= playable_span + 12:
            lookahead = 24
            switch_margin = 2
            shift_weight = 1.55
        else:
            lookahead = 32
            switch_margin = 3
            shift_weight = 1.75

        chord_dense = self.feat["avg_chord"] >= 2.0 or self.feat["max_chord"] >= 4
        high_pressure = self.feat["max_note"] > self.user_max
        low_pressure = self.feat["min_note"] < self.user_min
        melodic_busy = self.feat["avg_jump"] >= 8 or self.feat["max_jump"] >= 16
        short_ratio_008 = self.feat["short_ratio_008"]
        short_ratio_006 = self.feat["short_ratio_006"]

        right_edge = leftmost + window_size - 1
        shift_possible = self.user_max > right_edge
        auto_shift = True
        use_shift = shift_possible
        fixed_window = self.user_min >= leftmost and self.user_max <= right_edge
        if note_span <= window_size and self.feat["high_ratio"] < 0.10:
            use_shift = False
        if fixed_window:
            use_shift = False

        if short_ratio_006 >= 0.20:
            min_note_len = 0.06
        elif short_ratio_008 >= 0.18 or note_span > playable_span:
            min_note_len = 0.08
        else:
            min_note_len = 0.10

        preview_neighbors = 0
        if chord_dense and (high_pressure or melodic_busy):
            preview_neighbors = 2
        if self.feat["max_chord"] >= 5 and note_span > window_size:
            preview_neighbors = 4

        seed: Dict[str, Any] = {
            "LEFTMOST_NOTE": leftmost,
            "VISIBLE_OCTAVES": visible_octaves,
            "UNLOCKED_MIN_NOTE": self.user_min,
            "UNLOCKED_MAX_NOTE": self.user_max,
            "AUTO_TRANSPOSE": True,
            "AUTO_SHIFT_FROM_RANGE": auto_shift,
            "USE_SHIFT_OCTAVE": use_shift,
            "USE_PEDAL": any(t.has_pedal for t in self.analysis.track_infos),
            "LOOKAHEAD_NOTES": lookahead,
            "SWITCH_MARGIN": switch_margin,
            "MIN_NOTES_BETWEEN_SWITCHES": 10 if note_span <= playable_span + 6 else 14,
            "SHIFT_WEIGHT": shift_weight,
            "MIN_NOTE_LEN": min_note_len,
            "RETRIGGER_MODE": True,
            "RETRIGGER_PRIORITY": "latest" if chord_dense else "first",
            "RETRIGGER_GAP": 0.003,
            "PEDAL_ON_VALUE": _safe_int(self.current_config, "PEDAL_ON_VALUE", 64),
            "PEDAL_TAP_TIME": _safe_float(self.current_config, "PEDAL_TAP_TIME", 0.08),
            "CHORD_PRIORITY": chord_dense,
            "CHORD_SPLIT_THRESHOLD": self.threshold,
            "OCTAVE_FOLD_PRIORITY": True,
            "OCTAVE_FOLD_WEIGHT": 0.55 if not high_pressure else 0.68,
            "MAX_MELODIC_JUMP_AFTER_FOLD": 12 if not melodic_busy else 10,
            "BAR_AWARE_TRANSPOSE": (high_pressure or low_pressure) and not fixed_window,
            "BAR_TRANSPOSE_SCOPE": "phrase" if note_span <= playable_span + 12 else "halfbar",
            "BAR_TRANSPOSE_THRESHOLD": 1 if not high_pressure else 2,
            "MELODY_PRIORITY": True,
            "MELODY_PITCH_WEIGHT": 1.0,
            "MELODY_DURATION_WEIGHT": 0.7,
            "MELODY_CONTINUITY_WEIGHT": 1.2 if melodic_busy else 1.0,
            "MELODY_KEEP_TOP": 2 if self.feat["max_chord"] <= 4 else 3,
            "SHIFT_HOLD_BASS": (high_pressure and self.feat["low_ratio"] >= 0.10) and not fixed_window,
            "SHIFT_HOLD_MAX_NOTE": min(self.user_max, max(self.user_min, 59)),
            "SHIFT_HOLD_MAX_CHORD_RANK": 1,
            "SHIFT_HOLD_CONFLICT_CLEAR": True,
            "SHIFT_HOLD_RELEASE_DELAY": 0.03,
            "OCTAVE_AVOID_COLLISION": (chord_dense and (note_span > window_size or self.feat["max_chord"] >= 5)) and not fixed_window,
            "OCTAVE_PREVIEW_NEIGHBORS": 0 if fixed_window else preview_neighbors,
            "OCTAVE_LOOKAHEAD": lookahead,
        }
        return self._normalize_candidate(seed)

    def candidates(self, seed: Dict[str, Any]) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []
        heavy = self.total_group_count >= 300 or self.feat["note_count"] >= 2500
        fixed_window = self._is_fixed_window_candidate(seed)
        very_heavy = self.total_group_count >= 700 or self.feat["note_count"] >= 5500

        lookahead_deltas = (-6, 0, 6) if not heavy else ((-4, 0, 4) if not very_heavy else (0, 4))
        switch_deltas = (0,) if fixed_window else ((-1, 0, 1) if not very_heavy else (0, 1))
        fold_deltas = (-0.08, 0.0, 0.08) if not heavy else ((-0.06, 0.0) if not very_heavy else (0.0, 0.06))
        nav_deltas = (0.0,) if fixed_window else ((-0.15, 0.0, 0.15) if not heavy else ((-0.12, 0.0) if not very_heavy else (0.0, 0.12)))
        keep_deltas = (-1, 0, 1) if not heavy else ((0, 1) if not very_heavy else (0,))
        scope_choices = [seed["BAR_TRANSPOSE_SCOPE"], "phrase", "halfbar", "bar"]
        scope_choices = list(dict.fromkeys(scope_choices))[: (2 if heavy else 3)]
        if fixed_window:
            scope_choices = [seed["BAR_TRANSPOSE_SCOPE"]]
        min_note_len_deltas = (-0.02, 0.0, 0.02) if not heavy else ((-0.01, 0.0) if not very_heavy else (0.0, 0.01))

        lookahead_choices = sorted({max(8, int(seed["LOOKAHEAD_NOTES"]) + d) for d in lookahead_deltas})
        switch_choices = sorted({max(0, int(seed["SWITCH_MARGIN"]) + d) for d in switch_deltas})
        fold_weight_choices = sorted({round(min(0.95, max(0.35, float(seed["OCTAVE_FOLD_WEIGHT"]) + d)), 2) for d in fold_deltas})
        nav_weight_choices = sorted({round(min(2.1, max(1.0, float(seed["SHIFT_WEIGHT"]) + d)), 2) for d in nav_deltas})
        melody_keep_choices = sorted({max(1, min(4, int(seed["MELODY_KEEP_TOP"]) + d)) for d in keep_deltas})
        min_note_len_choices = sorted({round(min(0.14, max(0.05, float(seed["MIN_NOTE_LEN"]) + d)), 3) for d in min_note_len_deltas})

        for look in lookahead_choices:
            for switch_margin in switch_choices:
                for fold_w in fold_weight_choices:
                    for nav_w in nav_weight_choices:
                        for keep_top in melody_keep_choices:
                            for scope in scope_choices:
                                for min_note_len in min_note_len_choices:
                                    cand = dict(seed)
                                    cand["LOOKAHEAD_NOTES"] = look
                                    cand["SWITCH_MARGIN"] = switch_margin
                                    cand["OCTAVE_FOLD_WEIGHT"] = fold_w
                                    cand["SHIFT_WEIGHT"] = nav_w
                                    cand["MELODY_KEEP_TOP"] = keep_top
                                    cand["BAR_TRANSPOSE_SCOPE"] = scope
                                    cand["MIN_NOTE_LEN"] = min_note_len
                                    if fixed_window:
                                        cand["MIN_NOTES_BETWEEN_SWITCHES"] = int(seed["MIN_NOTES_BETWEEN_SWITCHES"])
                                        cand["USE_SHIFT_OCTAVE"] = False
                                    elif nav_w >= 1.75:
                                        cand["MIN_NOTES_BETWEEN_SWITCHES"] = max(6, int(seed["MIN_NOTES_BETWEEN_SWITCHES"]) - 2)
                                    elif nav_w <= 1.15:
                                        cand["MIN_NOTES_BETWEEN_SWITCHES"] = int(seed["MIN_NOTES_BETWEEN_SWITCHES"]) + 2
                                    else:
                                        cand["MIN_NOTES_BETWEEN_SWITCHES"] = int(seed["MIN_NOTES_BETWEEN_SWITCHES"])
                                    cand["OCTAVE_LOOKAHEAD"] = cand["LOOKAHEAD_NOTES"]
                                    candidates.append(self._normalize_candidate(cand))

        seen = set()
        unique: List[Dict[str, Any]] = []
        for cand in candidates:
            signature = (
                cand["LOOKAHEAD_NOTES"],
                cand["SWITCH_MARGIN"],
                cand["OCTAVE_FOLD_WEIGHT"],
                cand["SHIFT_WEIGHT"],
                cand["MELODY_KEEP_TOP"],
                cand["BAR_TRANSPOSE_SCOPE"],
                cand["MIN_NOTES_BETWEEN_SWITCHES"],
                cand["MIN_NOTE_LEN"],
            )
            if signature in seen:
                continue
            seen.add(signature)
            unique.append(cand)

        def _distance(cand: Dict[str, Any]) -> Tuple[float, float]:
            scope_rank = {"phrase": 0, "halfbar": 1, "bar": 2}
            d = 0.0
            d += abs(int(cand["LOOKAHEAD_NOTES"]) - int(seed["LOOKAHEAD_NOTES"])) / 4.0
            d += abs(int(cand["SWITCH_MARGIN"]) - int(seed["SWITCH_MARGIN"])) * 1.2
            d += abs(float(cand["OCTAVE_FOLD_WEIGHT"]) - float(seed["OCTAVE_FOLD_WEIGHT"])) * 10.0
            d += abs(float(cand["SHIFT_WEIGHT"]) - float(seed["SHIFT_WEIGHT"])) * 8.0
            d += abs(int(cand["MELODY_KEEP_TOP"]) - int(seed["MELODY_KEEP_TOP"])) * 1.0
            d += abs(scope_rank.get(str(cand["BAR_TRANSPOSE_SCOPE"]), 0) - scope_rank.get(str(seed["BAR_TRANSPOSE_SCOPE"]), 0)) * 1.3
            d += abs(int(cand["MIN_NOTES_BETWEEN_SWITCHES"]) - int(seed["MIN_NOTES_BETWEEN_SWITCHES"])) / 2.0
            d += abs(float(cand["MIN_NOTE_LEN"]) - float(seed["MIN_NOTE_LEN"])) * 40.0
            return (d, -float(cand["SHIFT_WEIGHT"]))

        max_candidates = 160
        if very_heavy:
            max_candidates = 48
        elif heavy:
            max_candidates = 64
        unique.sort(key=_distance)
        return unique[:max_candidates]

    def quick_score(
        self,
        cfg: Dict[str, Any],
        *,
        probe: bool = False,
        stop_above: Optional[float] = None,
    ) -> Tuple[float, Dict[str, Any]]:
        merged = self._normalize_candidate(cfg)
        group_indexes = self.probe_group_indexes if probe else self.full_eval_group_indexes
        return self._score_group_indexes(merged, group_indexes, stop_above=stop_above)

    def _advanced_refinement_candidates(self, best: Dict[str, Any]) -> List[Dict[str, Any]]:
        right_edge = int(best["LEFTMOST_NOTE"]) + int(best["VISIBLE_OCTAVES"]) * 12 - 1
        shift_needed_by_range = self.user_max > right_edge
        fixed_window = self._is_fixed_window_candidate(best)
        shift_choices = [bool(best.get("USE_SHIFT_OCTAVE", True))]
        if fixed_window:
            shift_choices = [False]
        elif shift_needed_by_range:
            shift_choices = list(dict.fromkeys(shift_choices + [True, False]))
        else:
            shift_choices = [False]

        auto_shift_choices = [bool(best.get("AUTO_SHIFT_FROM_RANGE", True))]
        if fixed_window:
            auto_shift_choices = [True]
        elif shift_needed_by_range:
            auto_shift_choices = list(dict.fromkeys(auto_shift_choices + [True, False]))
        else:
            auto_shift_choices = [True]

        heavy = self.total_group_count >= 300 or self.feat["note_count"] >= 2500
        very_heavy = self.total_group_count >= 700 or self.feat["note_count"] >= 5500

        collision_choices = [bool(best.get("OCTAVE_AVOID_COLLISION", False))]
        if fixed_window:
            collision_choices = [False]
        elif (self.feat["max_chord"] >= 4 or self.feat["avg_chord"] >= 2.0) and not very_heavy:
            collision_choices = list(dict.fromkeys(collision_choices + [True, False]))

        preview_seed = int(best.get("OCTAVE_PREVIEW_NEIGHBORS", 0))
        preview_deltas = (0, 2) if very_heavy else ((-2, 0, 2) if not heavy else (0, 2))
        preview_choices = sorted({max(0, preview_seed + d) for d in preview_deltas})
        preview_choices = [v for v in preview_choices if v <= 6] or [0]
        if fixed_window:
            preview_choices = [0]
        if 0 not in preview_choices:
            preview_choices.insert(0, 0)

        cooldown_deltas = (0, 2) if very_heavy else ((-2, 0, 2) if not heavy else (0, 2))
        cooldown_choices = sorted({max(0, int(best.get("MIN_NOTES_BETWEEN_SWITCHES", 12)) + d) for d in cooldown_deltas})
        min_note_len_deltas = (0.0, 0.01) if very_heavy else ((-0.01, 0.0, 0.01) if not heavy else (0.0, 0.01))
        min_note_len_choices = sorted({round(min(0.14, max(0.05, float(best.get("MIN_NOTE_LEN", 0.1)) + d)), 3) for d in min_note_len_deltas})

        refine: List[Dict[str, Any]] = []
        for use_shift in shift_choices:
            for auto_shift in auto_shift_choices:
                for collision in collision_choices:
                    for preview in preview_choices:
                        for cooldown in cooldown_choices:
                            for min_note_len in min_note_len_choices:
                                cand = dict(best)
                                cand["USE_SHIFT_OCTAVE"] = use_shift
                                cand["AUTO_SHIFT_FROM_RANGE"] = auto_shift
                                cand["OCTAVE_AVOID_COLLISION"] = collision
                                cand["OCTAVE_PREVIEW_NEIGHBORS"] = preview
                                cand["MIN_NOTES_BETWEEN_SWITCHES"] = cooldown
                                cand["MIN_NOTE_LEN"] = min_note_len
                                cand["OCTAVE_LOOKAHEAD"] = max(int(cand.get("LOOKAHEAD_NOTES", 24)), int(cand.get("OCTAVE_LOOKAHEAD", 0)))
                                refine.append(self._normalize_candidate(cand))
        return refine

    def tune(self) -> Tuple[Dict[str, Any], float, Dict[str, Any], int]:
        seed = self.build_seed()
        candidates = self.candidates(seed)
        tested = 0

        best = seed
        best_score, best_detail = self.quick_score(seed, probe=False)
        tested += 1

        probe_best = best_score
        probed: List[Tuple[float, Dict[str, Any]]] = []
        for cand in candidates:
            score, _detail = self.quick_score(cand, probe=True, stop_above=probe_best)
            tested += 1
            if score < probe_best:
                probe_best = score
            probed.append((score, cand))

        heavy = self.total_group_count >= 300 or self.feat["note_count"] >= 2500
        very_heavy = self.total_group_count >= 700 or self.feat["note_count"] >= 5500
        full_top_n = 4 if very_heavy else (6 if heavy else 12)
        top_candidates = [cand for _score, cand in sorted(probed, key=lambda item: item[0])[:full_top_n]]
        for cand in top_candidates:
            score, detail = self.quick_score(cand, probe=False, stop_above=best_score)
            if score < best_score:
                best = cand
                best_score = score
                best_detail = detail

        refine_candidates = self._advanced_refinement_candidates(best)
        refine_probed: List[Tuple[float, Dict[str, Any]]] = []
        refine_probe_best = best_score
        for cand in refine_candidates:
            score, _detail = self.quick_score(cand, probe=True, stop_above=refine_probe_best)
            tested += 1
            if score < refine_probe_best:
                refine_probe_best = score
            refine_probed.append((score, cand))
        refine_top_n = 3 if very_heavy else (4 if heavy else 8)
        for cand in [cand for _score, cand in sorted(refine_probed, key=lambda item: item[0])[:refine_top_n]]:
            score, detail = self.quick_score(cand, probe=False, stop_above=best_score)
            if score < best_score:
                best = cand
                best_score = score
                best_detail = detail

        final_best = self._normalize_candidate(best)
        best_detail = dict(best_detail)
        best_detail["probe_groups"] = len(self.probe_group_indexes)
        best_detail["full_groups"] = len(self.full_eval_group_indexes)
        best_detail["total_groups"] = len(self.groups)
        return final_best, best_score, best_detail, tested


def _serialize_preview_value(key: str, value: Any) -> str:
    if key.endswith("_NOTE"):
        return midi_to_note_name(int(value))
    if isinstance(value, bool):
        return "开启" if value else "关闭"
    return str(value)


def preview_lines(suggestions: Dict[str, Any]) -> List[str]:
    lines: List[str] = []
    for key, label in PREVIEW_LABELS:
        if key not in suggestions:
            continue
        lines.append(f"{label}：{_serialize_preview_value(key, suggestions[key])}")
    return lines


def suggest_config(
    analysis: MidiAnalysisResult,
    current_config: Dict[str, Any],
    playable_range: Optional[Tuple[int, int]] = None,
) -> Tuple[Dict[str, Any], str]:
    if not analysis.notes:
        return {}, "当前 MIDI 没有可用音符，无法自动调参。"

    if playable_range is None:
        user_min = _safe_int(current_config, "UNLOCKED_MIN_NOTE", 48)
        user_max = _safe_int(current_config, "UNLOCKED_MAX_NOTE", 83)
    else:
        user_min, user_max = playable_range
    if user_min > user_max:
        user_min, user_max = user_max, user_min

    tuner = MultiCandidateTuner(analysis, current_config, (user_min, user_max))
    best, best_score, best_detail, tested = tuner.tune()
    feat = tuner.feat
    filename = analysis.file_path.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]

    lines = [
        "自动调参建议（与当前播放逻辑同步评分）",
        f"- 文件：{filename}",
        f"- 音符数：{feat['note_count']}",
        f"- 原始音域：{midi_to_note_name(feat['min_note'])} ~ {midi_to_note_name(feat['max_note'])}",
        f"- 用户可弹奏区间：{midi_to_note_name(user_min)} ~ {midi_to_note_name(user_max)}",
        f"- 平均和弦数：{feat['avg_chord']:.2f}",
        f"- 最大和弦数：{feat['max_chord']}",
        f"- 高音占比：{feat['high_ratio'] * 100:.1f}%",
        f"- 低音占比：{feat['low_ratio'] * 100:.1f}%",
        f"- 平均旋律跳进：{feat['avg_jump']:.2f}",
        f"- 最大旋律跳进：{feat['max_jump']}",
        f"- 短音比例(≤0.08s)：{feat['short_ratio_008'] * 100:.1f}%",
        f"- 候选测试数：{tested}",
        f"- 快速预筛组数：{best_detail.get('probe_groups', len(tuner.probe_group_indexes))} / 精算组数：{best_detail.get('full_groups', len(tuner.full_eval_group_indexes))} / 总组数：{best_detail.get('total_groups', len(tuner.groups))}",
        f"- 最佳评分：{best_score:.2f}",
        f"- 估计漏音：{best_detail['lost']}",
        f"- 估计旋律损失：{best_detail['melody_loss']}",
        f"- 估计突兀折返：{best_detail['harsh_fold']}",
        f"- 估计切区次数：{best_detail['switch_need']}",
        f"- 估计防撞代价：{best_detail['collision_penalty']}",
        f"- 估计短音压缩代价：{best_detail['duration_penalty']}",
        f"- 固定窗口模式：{'开启' if best_detail.get('fixed_window_mode') else '关闭'}",
        "",
        "调参结论：",
        f"- 推荐基础窗口起点：{midi_to_note_name(int(best['LEFTMOST_NOTE']))}",
        f"- 推荐可见八度数：{best['VISIBLE_OCTAVES']}",
        f"- 推荐按音域自动判断右移窗口：{'开启' if best['AUTO_SHIFT_FROM_RANGE'] else '关闭'}",
        f"- 推荐启用右移窗口：{'开启' if best['USE_SHIFT_OCTAVE'] else '关闭'}",
        f"- 推荐固定窗口模式：{'开启' if (best['AUTO_SHIFT_FROM_RANGE'] and not best['USE_SHIFT_OCTAVE']) else '关闭'}",
        f"- 推荐预读音符数：{best['LOOKAHEAD_NOTES']}",
        f"- 推荐切换保守度：{best['SWITCH_MARGIN']}",
        f"- 推荐切区冷却：{best['MIN_NOTES_BETWEEN_SWITCHES']}",
        f"- 推荐右移窗口偏好：{best['SHIFT_WEIGHT']}",
        f"- 推荐最短按键时长：{best['MIN_NOTE_LEN']}",
        f"- 推荐启用防撞：{'开启' if best['OCTAVE_AVOID_COLLISION'] else '关闭'}",
        f"- 推荐邻近预览数量：{best['OCTAVE_PREVIEW_NEIGHBORS']}",
        f"- 推荐局部移八度范围：{best['BAR_TRANSPOSE_SCOPE']}",
        f"- 推荐旋律保留层数：{best['MELODY_KEEP_TOP']}",
    ]
    return best, "\n".join(lines)
