import sys
from sqlalchemy import inspect, text
from app import create_app
from models import db

EXPECTED_TABLES = [
    "department",
    "users",
    "course",
    "semester",
    "review",
    "material",
    "flag_reason",
    "flag",
    "password_reset_token",
]

app = create_app()

failures = []

with app.app_context():
    inspector = inspect(db.engine)
    existing_tables = set(inspector.get_table_names())

    for table in EXPECTED_TABLES:
        if table not in existing_tables:
            print(f"FAIL  {table}  [table not found in database]")
            failures.append(table)
            continue

        try:
            with db.engine.connect() as conn:
                conn.execute(text(f"SELECT 1 FROM `{table}` LIMIT 1"))
            print(f"PASS  {table}")
        except Exception as exc:
            print(f"FAIL  {table}  [{exc}]")
            failures.append(table)

if failures:
    print(f"\n{len(failures)} table(s) failed verification.")
    sys.exit(1)

print(f"\nAll {len(EXPECTED_TABLES)} tables verified successfully.")
sys.exit(0)
