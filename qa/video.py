"""테스트 녹화(webm) → Slack에서 바로 재생되는 mp4.

Playwright는 webm으로 녹화한다. Slack 인라인 재생과 호환성을 위해 H.264 mp4로 바꾸고,
AI 탐색처럼 생각하는 동안 화면이 멈춰 있는 긴 영상은 배속을 올린다.
ffmpeg는 시스템 설치 대신 imageio-ffmpeg에 함께 오는 바이너리를 쓴다.
"""

import logging
import subprocess
from pathlib import Path

log = logging.getLogger(__name__)


def to_mp4(src: Path, dst: Path, speed: float = 1.0, timeout: float = 300) -> Path | None:
    """변환에 실패해도 검증 결과는 그대로 둔다 — 영상은 사람이 보는 보조 증거다."""
    import imageio_ffmpeg  # 바이너리 경로 탐색이 있어 실제로 쓸 때만 불러온다

    if not src.is_file() or src.stat().st_size == 0:
        log.warning("녹화 파일 없음 또는 빈 파일: %s", src)
        return None
    vf = "scale=trunc(iw/2)*2:trunc(ih/2)*2"  # H.264는 가로·세로가 짝수여야 한다
    if speed != 1:
        vf = f"setpts=PTS/{speed},{vf}"
    # -nostdin·stdin=DEVNULL: ffmpeg는 기본으로 키 입력을 읽는다. 워커를 터미널에서 백그라운드로 띄우면
    # 터미널 입력을 읽으려다 SIGTTIN으로 워커 프로세스 그룹 전체가 멈춘다.
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-nostdin", "-y", "-loglevel", "error", "-i", str(src),
           "-vf", vf, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "28",
           "-movflags", "+faststart", str(dst)]
    try:
        out = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        log.warning("영상 변환 시간 초과: %s", src)
        return None
    if out.returncode != 0 or not dst.is_file():
        log.warning("영상 변환 실패: %s\n%s", src, out.stderr[-500:])
        return None
    return dst
