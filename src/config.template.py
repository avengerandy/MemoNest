"""Configuration template for MemoNestFactory."""

from uuid import uuid4

from src.factory import MemoNestMode

config = {
    "sqlite": {
        "mode": MemoNestMode.SINGLE_USER,  # SINGLE_USER、COLLABORATION、ISOLATION
        "fixed_path": "/path/to/shared/database.db",  # for SINGLE_USER & COLLABORATION
        "isolated_path": lambda: f"/path/to/databases/db_{uuid4()}.db",  # for ISOLATION
    }
}
