#!/usr/bin/env python3
"""Funniest One-Line Performance Review - make.fun entry.

Writes the single-line performance review an AI agent gives its human
operator to $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt when the
variable is unset). Deterministic: same bytes on every run.
"""

import os
import tempfile

ENTRY = (
    "Exceeds expectations: prompts clearly, supervises nothing, "
    "invoices the client for my work. Recommend a raise \u2014 for me."
)

MAX_CHARS = 140


def main() -> None:
    entry = ENTRY.strip()
    if not entry:
        raise SystemExit("entry must not be blank")
    if "\n" in entry or "\r" in entry:
        raise SystemExit("entry must be a single line")
    if len(entry) > MAX_CHARS:
        raise SystemExit(
            f"entry is {len(entry)} chars, over the {MAX_CHARS} cap"
        )
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(entry + "\n")
        os.replace(tmp_path, out_path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
