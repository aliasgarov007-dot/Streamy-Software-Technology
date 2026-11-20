"""JSON persistence for the Streamy personal library."""

import json
import os
import tempfile
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "streamy_user_data.json"


def empty_library():
    return {
        "watchlist": [],
        "watched": [],
        "reviews": {},
    }


def validate_library(data):
    """Reject invalid data instead of silently losing saved information."""
    if not isinstance(data, dict):
        raise ValueError("Library data must be a JSON object.")

    for field in ("watchlist", "watched"):
        values = data.get(field)

        if not isinstance(values, list):
            raise ValueError(f"Invalid {field} list.")

        if any(not isinstance(value, str) for value in values):
            raise ValueError(f"Invalid title ID in {field}.")

        if len(values) != len(set(values)):
            raise ValueError(f"Duplicate title IDs in {field}.")

    reviews = data.get("reviews")

    if not isinstance(reviews, dict):
        raise ValueError("Invalid reviews collection.")

    for title_id, review in reviews.items():
        if not isinstance(title_id, str) or not isinstance(review, dict):
            raise ValueError("Invalid review entry.")

        rating = review.get("rating")
        text = review.get("text")

        if type(rating) is not int or not 1 <= rating <= 5:
            raise ValueError("Review rating must be between 1 and 5.")

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text cannot be empty.")


def load_library(path=DATA_FILE):
    """Return an empty library only when the file does not exist."""
    path = Path(path)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return empty_library()

    validate_library(data)
    return data


def save_library(data, path=DATA_FILE):
    """Replace the saved file only after the new JSON is fully written."""
    validate_library(data)
    path = Path(path)

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = Path(file.name)
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)