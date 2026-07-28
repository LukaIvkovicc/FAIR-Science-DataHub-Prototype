from pathlib import Path

from app.database import SessionLocal, init_db
from app.services.ingestion import load_example_data


def main() -> None:
    init_db()
    data_dir = Path(__file__).resolve().parents[1] / "data"
    with SessionLocal() as db:
        summary = load_example_data(db, data_dir)
    print(f"Loaded example data: {summary}")


if __name__ == "__main__":
    main()

