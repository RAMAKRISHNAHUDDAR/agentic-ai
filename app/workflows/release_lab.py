"""Versioned local release simulator for a student attendance alert policy."""
import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DATABASE = Path(__file__).resolve().parents[2] / "data" / "lab_releases.db"


@contextmanager
def transaction():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    try:
        with db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("""CREATE TABLE IF NOT EXISTS releases (
                id INTEGER PRIMARY KEY, cutoff INTEGER, previous INTEGER,
                state TEXT, author TEXT, reviewer TEXT)""")
            db.execute("""CREATE TABLE IF NOT EXISTS events (
                release_id INTEGER, actor TEXT, action TEXT,
                created TEXT DEFAULT CURRENT_TIMESTAMP)""")
            yield db
    finally:
        db.close()


def implementation(cutoff):
    if type(cutoff) is not int or not 1 <= cutoff <= 100:
        raise ValueError("Invalid attendance threshold.")
    return f"def flag_attendance(attendance):\n    return attendance < {cutoff}\n"


def evaluate(cutoff, attendance):
    # Only a validated integer can enter this fixed, locally generated module.
    namespace = {"__builtins__": {}}
    exec(compile(implementation(cutoff), "<attendance-policy>", "exec"), namespace)
    return namespace["flag_attendance"](attendance)


def acceptance_cases(cutoff):
    return [(cutoff - 1, True), (cutoff, False), (100, False)]


def stage(requirement, actor):
    match = re.fullmatch(r"flag attendance below (\d{1,3})%\.?", requirement.strip(), re.I)
    if not match or not 1 <= int(match[1]) <= 100:
        raise ValueError("Specify a threshold from 1 to 100, for example 'Flag attendance below 65%'.")
    cutoff = int(match[1])
    cases = acceptance_cases(cutoff)
    if any(evaluate(cutoff, value) != expected for value, expected in cases):
        raise ValueError("Acceptance checks failed.")
    with transaction() as db:
        current = db.execute("SELECT id FROM releases WHERE state='active'").fetchone()
        release = db.execute("INSERT INTO releases(cutoff,previous,state,author) VALUES(?,?,'tested',?)",
                             (cutoff, current[0] if current else None, actor)).lastrowid
        db.execute("INSERT INTO events(release_id,actor,action) VALUES(?,?,?)",
                   (release, actor, "Requirement compiled to attendance rule. Boundary tests passed."))
    return release


def transition(release, action, actor, role):
    if role != "mentor" or not actor:
        raise PermissionError("A signed-in mentor must review release actions.")
    with transaction() as db:
        row = db.execute("SELECT * FROM releases WHERE id=?", (release,)).fetchone()
        active = db.execute("SELECT id FROM releases WHERE state='active'").fetchone()
        current = active[0] if active else None
        if action == "approve" and row and row["state"] == "tested" and row["previous"] == current:
            db.execute("UPDATE releases SET state='superseded' WHERE state='active'")
            db.execute("UPDATE releases SET state='active', reviewer=? WHERE id=?", (actor, release))
        elif action == "rollback" and row and row["state"] == "active":
            db.execute("UPDATE releases SET state='rolled_back' WHERE id=?", (release,))
            db.execute("UPDATE releases SET state='active' WHERE id=?", (row["previous"],))
        else:
            raise ValueError("Release state changed or action is invalid. Review the current version.")
        db.execute("INSERT INTO events(release_id,actor,action) VALUES(?,?,?)", (release, actor, action))


def snapshot():
    with transaction() as db:
        return [dict(r) for r in db.execute("SELECT * FROM releases ORDER BY id DESC")], [
            dict(r) for r in db.execute("SELECT * FROM events ORDER BY rowid DESC LIMIT 50")]
