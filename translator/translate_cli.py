"""CLI worker used by the GUI to isolate model inference in a child process."""

import argparse
import json
import sys

from translator.translation_thread import translate_text


def _configure_stdio():
    """Force UTF-8 stdio so Chinese text survives subprocess boundaries on Windows."""
    for stream_name in ("stdin", "stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def main():
    try:
        _configure_stdio()
        parser = argparse.ArgumentParser()
        parser.add_argument("--text")
        parser.add_argument("--source-lang")
        parser.add_argument("--target-lang")
        args = parser.parse_args()

        if args.text is not None:
            text = args.text
            source_lang = args.source_lang
            target_lang = args.target_lang
        else:
            payload = json.loads(sys.stdin.read())
            text = payload["text"]
            source_lang = payload["source_lang"]
            target_lang = payload["target_lang"]

        result = translate_text(text, source_lang, target_lang)
        sys.stdout.write(json.dumps({"ok": True, "result": result}, ensure_ascii=False))
    except Exception as exc:
        sys.stdout.write(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
