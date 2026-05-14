#!/usr/bin/env python3
"""Download a Xiaoyuzhou episode and generate SRT/TXT via faster-whisper."""

import argparse
import json
import re
import sys
from pathlib import Path

import requests


def fetch_html(url: str) -> str:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def extract_next_data(html: str) -> dict:
    match = re.search(
        r'__NEXT_DATA__" type="application/json">(.*?)</script>',
        html,
        re.DOTALL,
    )
    if not match:
        raise RuntimeError("Could not find __NEXT_DATA__ in page")
    return json.loads(match.group(1))


def find_episode(next_data: dict) -> dict:
    page_props = next_data.get("props", {}).get("pageProps", {})
    episode = page_props.get("episode")
    if episode:
        return episode
    for query in page_props.get("dehydratedState", {}).get("queries", []):
        if not isinstance(query, dict):
            continue
        state = query.get("state") if isinstance(query.get("state"), dict) else None
        data = state.get("data") if state else None
        if isinstance(data, dict) and isinstance(data.get("episode"), dict):
            return data["episode"]
    raise RuntimeError("Could not locate episode data in page")


def extract_audio_url(episode: dict) -> str:
    candidates = [
        ("enclosure", "url"),
        ("media", "source", "url"),
    ]
    for path in candidates:
        node = episode
        ok = True
        for key in path:
            if not isinstance(node, dict) or key not in node:
                ok = False
                break
            node = node[key]
        if ok and isinstance(node, str) and node.startswith("http"):
            return node
    raise RuntimeError("Could not find audio URL in episode data")


def derive_basename(url: str, episode: dict) -> str:
    eid = episode.get("eid") or episode.get("id")
    if isinstance(eid, str) and eid.strip():
        return f"xiaoyuzhou-{eid.strip()}"
    match = re.search(r"/episode/([A-Za-z0-9]+)", url)
    if match:
        return f"xiaoyuzhou-{match.group(1)}"
    return "xiaoyuzhou-episode"


def download_file(url: str, dest_path: Path, force: bool = False) -> None:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = dest_path.with_suffix(dest_path.suffix + ".part")

    if dest_path.exists() and not force:
        return

    headers = {}
    mode = "wb"
    if temp_path.exists() and not force:
        existing = temp_path.stat().st_size
        if existing > 0:
            headers["Range"] = f"bytes={existing}-"
            mode = "ab"

    with requests.get(url, stream=True, timeout=30, headers=headers) as resp:
        if resp.status_code == 200 and "Range" in headers:
            mode = "wb"
        resp.raise_for_status()
        with open(temp_path, mode) as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    temp_path.replace(dest_path)


def format_timestamp(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    ms_total = int(round(seconds * 1000))
    hours = ms_total // 3600000
    ms_total %= 3600000
    minutes = ms_total // 60000
    ms_total %= 60000
    seconds = ms_total // 1000
    ms = ms_total % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"


def write_srt(segments, srt_path: Path) -> None:
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start = format_timestamp(seg.start)
            end = format_timestamp(seg.end)
            text = seg.text.strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def write_txt(segments, txt_path: Path) -> None:
    lines = [seg.text.strip() for seg in segments if seg.text.strip()]
    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download Xiaoyuzhou episode audio and generate SRT/TXT.")
    parser.add_argument("url", help="Xiaoyuzhou episode URL")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    parser.add_argument("--model", default="tiny", help="Whisper model size")
    parser.add_argument("--language", default=None, help="Language code or auto")
    parser.add_argument("--device", default="cpu", help="Device: cpu or cuda")
    parser.add_argument(
        "--compute-type",
        default="int8",
        help="Compute type, e.g. int8, int8_float16, float16",
    )
    parser.add_argument("--beam-size", type=int, default=1, help="Beam size")
    parser.add_argument("--no-vad", action="store_true", help="Disable VAD")
    parser.add_argument(
        "--audio-path",
        default=None,
        help="Use an existing audio file instead of downloading",
    )
    parser.add_argument(
        "--force-download", action="store_true", help="Re-download audio"
    )

    args = parser.parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.audio_path:
        audio_path = Path(args.audio_path).expanduser().resolve()
        if not audio_path.exists():
            print(f"Audio path not found: {audio_path}", file=sys.stderr)
            return 1
        base_name = audio_path.stem
    else:
        html = fetch_html(args.url)
        next_data = extract_next_data(html)
        episode = find_episode(next_data)
        audio_url = extract_audio_url(episode)
        base_name = derive_basename(args.url, episode)
        audio_path = output_dir / f"{base_name}.mp3"
        download_file(audio_url, audio_path, force=args.force_download)

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print(
            "Missing dependency: faster-whisper. Install with: \n"
            "  python3 -m pip install -U faster-whisper",
            file=sys.stderr,
        )
        return 1

    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=args.compute_type,
    )
    segments, info = model.transcribe(
        str(audio_path),
        beam_size=args.beam_size,
        language=args.language,
        vad_filter=not args.no_vad,
    )

    segments = list(segments)
    srt_path = output_dir / f"{base_name}.srt"
    txt_path = output_dir / f"{base_name}.txt"

    write_srt(segments, srt_path)
    write_txt(segments, txt_path)

    print(f"language: {info.language} (p={info.language_probability:.2f})")
    print(f"audio: {audio_path}")
    print(f"srt:   {srt_path}")
    print(f"txt:   {txt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
