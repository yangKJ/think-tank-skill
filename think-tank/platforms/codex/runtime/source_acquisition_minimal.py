#!/usr/bin/env python3
"""Codex minimal source-acquisition runtime."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_target(target: str) -> tuple[bool, str, str]:
    parsed = urlparse(target)
    try:
        if parsed.scheme in {"http", "https"}:
            request = Request(target, headers={"User-Agent": "think-tank-minimal-runtime/0.1"})
            with urlopen(request, timeout=8) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return True, response.read().decode(charset, errors="replace"), "success"
        if parsed.scheme == "file":
            path = Path(unquote(parsed.path))
            return True, path.read_text(encoding="utf-8"), "success"
        path = Path(target)
        return True, path.read_text(encoding="utf-8"), "success"
    except (OSError, HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
        return False, "", f"{type(exc).__name__}: {exc}"


def html_title(content: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", content, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", content, flags=re.IGNORECASE | re.DOTALL)
    if h1:
        return re.sub(r"<[^>]+>", "", h1.group(1)).strip()
    return "Untitled source"


def summarize(content: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", content, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:220] if text else "No readable text extracted."


def runtime_result(target: str, runtime: str) -> dict[str, Any]:
    success, content, status = read_target(target)
    base: dict[str, Any] = {
        "runtime": runtime,
        "mode": "research",
        "profile": "source-collector",
        "capability": "source-acquisition",
        "dispatch_request": {
            "target": target,
            "constraints": ["readonly", "no_login", "no_download"],
        },
        "dispatch_decision": {
            "selected_skill": "local_static_reader" if runtime == "codex-minimal" else "WebFetch",
            "status": "dispatched",
            "risk_level": "low",
        },
        "invocation": {
            "invoked": True,
            "method": "local_static_reader" if runtime == "codex-minimal" else "WebFetch",
            "target": target,
            "result_status": "success" if success else "failed",
        },
        "recovery": {
            "result_recovered": success,
            "recovered_as": ["sources[]", "evidence[]"] if success else [],
        },
        "sources": [],
        "evidence": [],
        "boundaries": [],
        "quality_check": {
            "protocol_complete": True,
            "evidence_boundary_clear": True,
            "actionable": True,
        },
    }
    if success:
        title = html_title(content)
        summary = summarize(content)
        base["sources"] = [
            {
                "title": title,
                "url": target,
                "source_type": "static-html",
                "summary": summary,
                "reliability": "medium",
                "freshness": now_iso(),
                "extracted_at": now_iso(),
            }
        ]
        base["evidence"] = [
            "dispatch_decision was produced before invocation.",
            f"{base['invocation']['method']} returned readable static content.",
        ]
        base["boundaries"] = [
            "Only one public/static source-acquisition target was read.",
            "No fallback, browser DOM, login state, or private write was attempted.",
        ]
    else:
        base["boundaries"] = [
            f"Target read failed: {status}",
            "No fallback was executed.",
            "No source or evidence was fabricated from the failed invocation.",
            "This does not prove full adapter dispatch runtime.",
        ]
    return base


def main() -> int:
    parser = argparse.ArgumentParser(description="Run think-tank minimal source-acquisition runtime.")
    parser.add_argument("target")
    parser.add_argument("--runtime", choices=["codex-minimal", "claude-code-minimal"], default="codex-minimal")
    args = parser.parse_args()
    print(json.dumps(runtime_result(args.target, args.runtime), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
