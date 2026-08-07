#!/usr/bin/env python3
"""
Setup helper that downloads ML models only when their packages are present.
This avoids build failures when optional heavy packages are excluded from
`requirements.txt` for lightweight deployments.
"""
import subprocess
import sys


def install_spacy_model():
    try:
        import spacy
    except Exception:
        print("spaCy not installed; skipping model download.")
        return

    try:
        from spacy.cli import download
        model = "en_core_web_sm"
        print(f"Downloading spaCy model {model}...")
        download(model)
        print("spaCy model download complete.")
    except Exception as exc:
        print("spaCy model download failed:", exc)


if __name__ == "__main__":
    install_spacy_model()
