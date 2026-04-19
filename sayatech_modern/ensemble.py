from __future__ import annotations

import socket
import struct
from datetime import datetime, timedelta, timezone
from statistics import median
from typing import List, Tuple
from urllib import request as urllib_request
from email.utils import parsedate_to_datetime

BEIJING_TZ = timezone(timedelta(hours=8), name="CST")
NTP_EPOCH = 2208988800
NTP_SOURCES: List[Tuple[str, str]] = [
    ("阿里云NTP-1", "time1.aliyun.com"),
    ("阿里云NTP-2", "time2.aliyun.com"),
    ("腾讯云NTP-1", "ntp.tencent.com"),
    ("腾讯云NTP-2", "ntp1.tencent.com"),
]
HTTP_SOURCES: List[Tuple[str, str]] = [
    ("BJTime", "https://www.bjtime.org.cn/"),
    ("中科院时间", "https://www.time.ac.cn/"),
    ("百度", "https://www.baidu.com/"),
]


def _fetch_ntp_offset(host: str, timeout: float = 1.5) -> float:
    packet = b"\x1b" + 47 * b"\0"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        start = datetime.now(timezone.utc).timestamp()
        sock.sendto(packet, (host, 123))
        data, _ = sock.recvfrom(48)
        end = datetime.now(timezone.utc).timestamp()
    finally:
        sock.close()
    if len(data) < 48:
        raise ValueError("NTP 数据过短")
    unpacked = struct.unpack("!12I", data[:48])
    transmit_ts = unpacked[10] + unpacked[11] / 4294967296.0
    server_ts = transmit_ts - NTP_EPOCH
    midpoint_local = start + (end - start) / 2.0
    return server_ts - midpoint_local


def _fetch_http_offset(url: str, timeout: float = 3.0) -> float:
    req = urllib_request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
    start = datetime.now(timezone.utc).timestamp()
    with urllib_request.urlopen(req, timeout=timeout) as resp:
        end = datetime.now(timezone.utc).timestamp()
        date_header = resp.headers.get("Date")
        if not date_header:
            raise ValueError("HTTP Date 头缺失")
        dt = parsedate_to_datetime(date_header)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        server_ts = dt.timestamp()
    midpoint_local = start + (end - start) / 2.0
    return server_ts - midpoint_local


def sync_beijing_clock() -> tuple[float, str, str]:
    offsets: List[tuple[float, str]] = []
    errors: List[str] = []
    for name, host in NTP_SOURCES:
        try:
            offsets.append((_fetch_ntp_offset(host), name))
        except Exception as exc:  # pragma: no cover - network dependent
            errors.append(f"{name}: {exc}")
    mode = "NTP"
    if not offsets:
        mode = "HTTP回退"
        for name, url in HTTP_SOURCES:
            try:
                offsets.append((_fetch_http_offset(url), name))
            except Exception as exc:  # pragma: no cover - network dependent
                errors.append(f"{name}: {exc}")
    if offsets:
        values = [item[0] for item in offsets]
        med = float(median(values))
        trusted = [name for offset, name in offsets if abs(offset - med) <= 1.0]
        source = " + ".join(trusted) if trusted else offsets[0][1]
        return med, f"{mode} | {source}", "校时成功"
    return 0.0, "本地时间", ("；".join(errors[-2:]) if errors else "校时失败，已回退本地时间")


def beijing_now(offset_sec: float) -> datetime:
    return datetime.fromtimestamp(datetime.now(timezone.utc).timestamp() + offset_sec, tz=BEIJING_TZ)
