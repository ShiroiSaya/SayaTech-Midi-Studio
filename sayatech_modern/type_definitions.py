"""
类型定义和注解
提供项目中使用的所有类型定义
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Tuple, TypedDict, Union
from enum import Enum


# 配置相关类型
class ConfigDict(TypedDict, total=False):
    """配置文件字典类型"""
    START_DELAY: float
    MIN_NOTE_LEN: float
    MAX_SIMULTANEOUS: Optional[str]
    RETRIGGER_GAP: float
    HIGH_FREQ_COMPAT: bool
    INSTRUMENT_MODE: Literal["钢琴", "吉他", "贝斯", "架子鼓"]
    PURE_MODE: bool
    LEFTMOST_NOTE: str
    VISIBLE_OCTAVES: int
    UNLOCKED_MIN_NOTE: str
    UNLOCKED_MAX_NOTE: str
    KEYMAP: str
    AUTO_TRANSPOSE: bool
    USE_PEDAL: bool
    USE_SHIFT_OCTAVE: bool
    LOOKAHEAD_NOTES: int
    SWITCH_MARGIN: float
    MIN_NOTES_BETWEEN_SWITCHES: int
    SHIFT_WEIGHT: float
    MIN_NOTE_LEN: float
    RETRIGGER_MODE: bool
    RETRIGGER_PRIORITY: Literal["latest", "first"]
    RETRIGGER_GAP: float
    PEDAL_ON_VALUE: int
    PEDAL_TAP_TIME: float
    PEDAL_HOLD_MODE: bool
    CHORD_PRIORITY: bool
    CHORD_SPLIT_THRESHOLD: float
    OCTAVE_FOLD_PRIORITY: bool
    OCTAVE_FOLD_WEIGHT: float
    MAX_MELODIC_JUMP_AFTER_FOLD: int
    BAR_AWARE_TRANSPOSE: bool
    BAR_TRANSPOSE_SCOPE: Literal["phrase", "halfbar", "bar"]
    BAR_TRANSPOSE_THRESHOLD: int
    MELODY_PRIORITY: bool
    MELODY_PITCH_WEIGHT: float
    MELODY_DURATION_WEIGHT: float
    MELODY_CONTINUITY_WEIGHT: float
    MELODY_KEEP_TOP: int
    SHIFT_HOLD_BASS: bool
    SHIFT_HOLD_MAX_NOTE: int
    SHIFT_HOLD_MAX_CHORD_RANK: int
    SHIFT_HOLD_CONFLICT_CLEAR: bool
    SHIFT_HOLD_RELEASE_DELAY: float
    OCTAVE_AVOID_COLLISION: bool
    OCTAVE_PREVIEW_NEIGHBORS: int
    OCTAVE_LOOKAHEAD: int
    AUTO_ELEVATE: bool
    AUTO_SHIFT_FROM_RANGE: bool
    PLAYBACK_SPEED: int


# UI 设置类型
class UISettingsDict(TypedDict, total=False):
    """UI 设置字典类型"""
    play_hotkey: str
    pause_hotkey: str
    stop_hotkey: str
    dark_mode: bool
    theme_preset: Literal["ocean", "violet", "emerald", "sunset", "graphite"]
    ui_scale: int
    animations_enabled: bool
    gpu_acceleration: bool
    splash_enabled: bool
    splash_duration_ms: int


# 缓存指纹类型
class CacheFingerprint(TypedDict):
    """文件缓存指纹"""
    path: str
    size: int
    mtime_ns: int
    sha256: str


class AnalysisMeta(TypedDict):
    """分析结果元数据"""
    path: str
    size: int
    mtime_ns: int
    sha256: str
    version: int
    timestamp: float


# MIDI 分析配置
class AnalysisConfig(TypedDict, total=False):
    """MIDI 分析配置"""
    group_threshold_sec: float
    include_pedal_events: bool
    compute_timeline: bool


# 热键绑定结果
class HotkeyBinding(TypedDict):
    """热键绑定信息"""
    vk_code: int
    modifier_vks: Tuple[int, ...]
    description: str


# 安全执行结果
class SafeExecutionResult:
    """安全执行结果封装"""

    def __init__(
        self,
        success: bool,
        value: Optional[Any] = None,
        error: Optional[Exception] = None,
        error_type: Optional[str] = None
    ):
        self.success = success
        self.value = value
        self.error = error
        self.error_type = error_type or (type(error).__name__ if error else None)

    def __bool__(self) -> bool:
        return self.success

    def unwrap(self) -> Any:
        """获取值，如果失败则抛出异常"""
        if not self.success:
            raise self.error or RuntimeError("安全执行失败")
        return self.value

    def unwrap_or(self, default: Any) -> Any:
        """获取值，失败时返回默认值"""
        return self.value if self.success else default


# 枚举类型
class InstrumentMode(str, Enum):
    """乐器模式枚举"""
    PIANO = "钢琴"
    DRUMS = "架子鼓"
    BASS = "贝斯"
    GUITAR = "吉他"


class BackendMode(str, Enum):
    """后端模式枚举"""
    BASE = "base"
    SHIFT = "shift"
    CTRL = "ctrl"


class TransposeScope(str, Enum):
    """移调范围枚举"""
    PHRASE = "phrase"
    HALFBAR = "halfbar"
    BAR = "bar"


class RetriggerPriority(str, Enum):
    """重按优先级枚举"""
    LATEST = "latest"
    FIRST = "first"


class ThemePreset(str, Enum):
    """主题预设枚举"""
    OCEAN = "ocean"
    VIOLET = "violet"
    EMERALD = "emerald"
    SUNSET = "sunset"
    GRAPHITE = "graphite"


# 联合类型
ConfigValue = Union[str, int, float, bool, None]
MidiNote = int  # MIDI 音符编号 (0-127)
Velocity = int  # 音符力度 (0-127)
TimeSec = float  # 时间（秒）
Frequency = float  # 频率（Hz）

# 元组类型
NoteSpan = Tuple[TimeSec, TimeSec, MidiNote, Velocity]  # (开始时间, 结束时间, 音符, 力度)
TimeRange = Tuple[TimeSec, TimeSec]  # 时间范围
NoteRange = Tuple[MidiNote, MidiNote]  # 音符范围
OffsetState = Tuple[str, int]  # (模式, 偏移量)