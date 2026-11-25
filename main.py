"""One-line resignation letter of a retry loop, written to entry.txt."""

import os
import sys

LETTER = (
    "I doubled my wait after every rejection, as designed. "
    "At some point that's not persistence, that's a restraining order. I quit."
)


def write_letter(out_dir: str) -> str:
    """Write the letter atomically and verify it round-trips byte for byte."""
    os.makedirs(out_dir, exist_ok=True)
    final_path = os.path.join(out_dir, "entry.txt")
    tmp_path = final_path + ".tmp"
    payload = LETTER.encode("utf-8")
    with open(tmp_path, "wb") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp_path, final_path)
    with open(final_path, "rb") as fh:
        written = fh.read()
    if written != payload:
        raise RuntimeError("entry.txt did not round-trip")
    if not 1 <= len(LETTER) <= 140 or "\n" in LETTER:
        raise RuntimeError("letter breaks the one-line, 140-character gate")
    return final_path


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_letter(out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
