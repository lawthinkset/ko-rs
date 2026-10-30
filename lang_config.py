"""Per-language configuration loader.

Each bot folder contains a language.json file. Import LANG from here
instead of hardcoding Russian (or any other language) strings.
"""

import json
from pathlib import Path


def load_lang_config():
    cfg_path = Path(__file__).resolve().parent / "language.json"
    with open(cfg_path, encoding="utf-8") as f:
        return json.load(f)


LANG = load_lang_config()
