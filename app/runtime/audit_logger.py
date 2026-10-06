import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
AUDIT_FILE = BASE_DIR / "data" / "audit_log.json"


def _ensure_audit_file():
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not AUDIT_FILE.exists():
        AUDIT_FILE.write_text("[]", encoding="utf-8")


def log_action(student_id, agent, action, result):
    """Store an audit record for an agent action."""
    _ensure_audit_file()

    records = json.loads(
        AUDIT_FILE.read_text(encoding="utf-8")
    )

    record = {
        "student_id": student_id,
        "agent": agent,
        "action": action,
        "result": result,
        "timestamp": datetime.now().isoformat(),
    }

    records.append(record)

    AUDIT_FILE.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8"
    )

    return record


def get_audit_logs(student_id=None):
    """Retrieve audit records, optionally filtered by student."""
    _ensure_audit_file()

    records = json.loads(
        AUDIT_FILE.read_text(encoding="utf-8")
    )

    if student_id is None:
        return records

    return [
        record
        for record in records
        if record.get("student_id") == student_id
    ]