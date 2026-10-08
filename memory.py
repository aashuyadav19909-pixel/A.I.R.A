import json
from pathlib import Path


MEMORY_FOLDER = Path("memory")
MEMORY_FILE = MEMORY_FOLDER / "memory.json"


# ============================================================
# SETUP
# ============================================================

def setup_memory():

    MEMORY_FOLDER.mkdir(exist_ok=True)

    if not MEMORY_FILE.exists():

        MEMORY_FILE.write_text(
            '{"facts": {}}',
            encoding="utf-8"
        )


# ============================================================
# NORMALIZE KEY
# ============================================================

def normalize_key(key):

    key = key.lower().strip()

    prefixes = [
        "my ",
        "your ",
        "the "
    ]

    for prefix in prefixes:

        if key.startswith(prefix):

            key = key[len(prefix):]

    return key.strip()


# ============================================================
# LOAD
# ============================================================

def load_memory():

    setup_memory()

    try:

        data = json.loads(
            MEMORY_FILE.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, dict):
            data = {"facts": {}}

        if "facts" not in data:
            data["facts"] = {}

        return data

    except Exception:

        return {
            "facts": {}
        }


# ============================================================
# SAVE
# ============================================================

def save_memory(data):

    setup_memory()

    MEMORY_FILE.write_text(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


# ============================================================
# REMEMBER
# ============================================================

def remember(key, value):

    key = normalize_key(key)

    value = value.strip()

    data = load_memory()

    data["facts"][key] = value

    save_memory(data)

    return f"I'll remember that your {key} is {value}."


# ============================================================
# RECALL
# ============================================================

def recall(key):

    key = normalize_key(key)

    data = load_memory()

    return data["facts"].get(key)


# ============================================================
# GET ALL MEMORIES
# ============================================================

def get_all_memory():

    data = load_memory()

    return data.get("facts", {})


# ============================================================
# FORGET
# ============================================================

def forget(key):

    key = normalize_key(key)

    data = load_memory()

    if key in data["facts"]:

        del data["facts"][key]

        save_memory(data)

        return f"I forgot your {key}."

    return f"I don't have anything saved about your {key}."


# ============================================================
# CLEAR ALL
# ============================================================

def clear_memory():

    data = {
        "facts": {}
    }

    save_memory(data)

    return "I've cleared all saved memories."