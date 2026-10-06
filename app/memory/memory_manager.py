import json
from pathlib import Path


MEMORY_FILE = Path("data/intervention_memory.json")


def _ensure_memory_file():
    """Create the memory file if it does not exist."""
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not MEMORY_FILE.exists():
        MEMORY_FILE.write_text("[]", encoding="utf-8")


def load_memory():
    """Load all stored intervention records."""
    _ensure_memory_file()

    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_memory(records):
    """Save intervention records to persistent memory."""
    _ensure_memory_file()

    MEMORY_FILE.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8"
    )


def add_memory(record):
    """Add one intervention record to memory."""
    records = load_memory()
    records.append(record)
    save_memory(records)

    return record


def get_student_memory(student_id):
    """Return intervention history for a student."""
    records = load_memory()

    return [
        record
        for record in records
        if record.get("student_id") == student_id
    ]