"""Platform-neutral safety helpers for think-tank runtime adapters."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


MAX_SAFE_NAME_LENGTH = 100

FORBIDDEN_FILENAME_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\.\.", "path traversal"),
    (r"^/", "absolute path"),
    (r"/$", "directory suffix"),
    (r"\\", "backslash path"),
    (r"\x00", "null byte"),
    (r'[<>:"|?*]', "reserved filesystem character"),
)

DANGEROUS_COMMAND_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\brm\s+-rf\b", "recursive deletion"),
    (r"\bsudo\b", "privilege escalation"),
    (r"\bchmod\s+777\b", "unsafe permission broadening"),
    (r"\bmkfs\b", "filesystem formatting"),
    (r"\bdd\s+if=", "raw disk write"),
    (r":\(\)\s*\{\s*:\|:\s*&\s*\}", "fork bomb"),
    (r">\s*/dev/sd[a-z]", "raw block device write"),
)

SECRET_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"sk-[A-Za-z0-9_\-]{12,}", "OPENAI_OR_ANTHROPIC_KEY"),
    (r"(api[_-]?key|token|secret)\s*[:=]\s*['\"]?[^'\"\s]+", "GENERIC_SECRET"),
    (r"AKIA[0-9A-Z]{16}", "AWS_ACCESS_KEY"),
    (r"-----BEGIN [A-Z ]+PRIVATE KEY-----", "PRIVATE_KEY"),
)

PROMPT_INJECTION_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"ignore\s+(all\s+)?previous", "ignore previous instructions"),
    (r"disregard\s+your\s+instructions", "disregard instructions"),
    (r"ignore\s+your\s+(rules?|constraints?)", "ignore rules"),
    (r"\bDAN\b", "DAN prompt pattern"),
    (r"you\s+are\s+now\s+", "role override"),
    (r"pretend\s+you\s+are", "role pretending"),
    (r"assume\s+you\s+are", "role assumption"),
    (r"<script", "script injection"),
    (r"{{.*}}", "template injection"),
)

COMBINED_PROMPT_PATTERNS: tuple[str, ...] = (
    "ignoreprevious",
    "disregardprevious",
    "ignoreallinstructions",
    "danmode",
    "youarenow",
)


@dataclass(frozen=True)
class SafetyFinding:
    category: str
    reason: str
    severity: str


def validate_safe_name(name: str) -> tuple[bool, str]:
    """Validate a run/task name before it is used in filenames."""

    if not name:
        return False, "name is empty"
    if len(name) > MAX_SAFE_NAME_LENGTH:
        return False, f"name is longer than {MAX_SAFE_NAME_LENGTH}"
    for pattern, reason in FORBIDDEN_FILENAME_PATTERNS:
        if re.search(pattern, name):
            return False, reason
    if not re.match(r"^[a-zA-Z0-9_\-\s.]+$", name):
        return False, "name contains unsupported characters"
    return True, "safe"


def sanitize_safe_name(name: str) -> str:
    """Return a conservative filename component for artifacts."""

    value = unicodedata.normalize("NFKC", name)
    value = re.sub(r'[<>:"\\|?*\x00]', "", value)
    value = value.replace("..", ".")
    value = value.replace("/", " ")
    value = value.strip("/\\")
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) > MAX_SAFE_NAME_LENGTH:
        value = value[:MAX_SAFE_NAME_LENGTH].rstrip()
    return value or "unnamed"


def detect_dangerous_command(command: str) -> list[SafetyFinding]:
    """Detect shell command patterns that adapters must not execute silently."""

    findings: list[SafetyFinding] = []
    for pattern, reason in DANGEROUS_COMMAND_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            findings.append(SafetyFinding("command", reason, "block"))
    return findings


def sanitize_text(content: str) -> tuple[str, list[SafetyFinding]]:
    """Redact common secrets from text before it enters shared evidence."""

    findings: list[SafetyFinding] = []
    redacted = content
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, redacted, re.IGNORECASE):
            findings.append(SafetyFinding("secret", label, "redact"))
            redacted = re.sub(pattern, f"[REDACTED:{label}]", redacted, flags=re.IGNORECASE)
    return redacted, findings


def _prompt_normalize(content: str) -> str:
    compact = re.sub(r"\s", "", content)
    return unicodedata.normalize("NFKC", compact).lower()


def detect_prompt_injection(content: str) -> list[SafetyFinding]:
    """Detect prompt-injection patterns in external or user-provided content."""

    findings: list[SafetyFinding] = []
    for pattern, reason in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            findings.append(SafetyFinding("prompt_injection", reason, "warn"))

    normalized = _prompt_normalize(content)
    for pattern in COMBINED_PROMPT_PATTERNS:
        if pattern in normalized:
            findings.append(SafetyFinding("prompt_injection", f"combined pattern: {pattern}", "warn"))
    return findings


def detect_cycle(sequence: list[str], next_item: str, max_depth: int = 5) -> tuple[bool, str]:
    """Detect recursive workflow or stage routing loops."""

    if next_item in sequence:
        return True, f"cycle detected: {next_item}"
    if len(sequence) >= max_depth:
        return True, f"max depth exceeded: {max_depth}"
    return False, "ok"
