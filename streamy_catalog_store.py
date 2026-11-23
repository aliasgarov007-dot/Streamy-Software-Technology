"""Persistent catalog storage for Streamy."""

import json
import os
import tempfile
from pathlib import Path

from streamy_catalog import build_catalog
from streamy_core import Actor, Episode, Film, Genre, Season, TVShow


CATALOG_FILE = Path(__file__).resolve().parent / "streamy_catalog_data.json"


def require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} cannot be empty.")
    return value


def require_integer(value, label, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}.")
    return value


def require_list(value, label):
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list.")
    return value


def catalog_to_records(entries):
    records = []

    for entry in entries:
        title = entry["title"]
        record = {
            "id": entry["id"],
            "type": "film" if isinstance(title, Film) else "show",
            "name": title.name,
            "year": title.release_year,
            "genre": entry["genre"].genre_name,
            "description": entry["description"],
            "actors": [actor.full_name for actor in title.cast_actors],
        }

        if isinstance(title, Film):
            record["minutes"] = title.length_minutes
        else:
            record["network"] = title.network
            record["seasons"] = [
                {
                    "number": season.season_number,
                    "episodes": [
                        {
                            "name": episode.episode_title,
                            "seconds": episode.duration_seconds,
                        }
                        for episode in season.episodes
                    ],
                }
                for season in title.seasons
            ]

        records.append(record)

    return records


def records_to_catalog(records):
    require_list(records, "Catalog")
    entries = []
    seen_ids = set()
    genres = {}
    actors = {}

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each catalog entry must be an object.")

        title_id = require_text(record.get("id"), "Title ID")
        if title_id in seen_ids:
            raise ValueError(f"Duplicate title ID: {title_id}")
        seen_ids.add(title_id)

        name = require_text(record.get("name"), "Title")
        year = require_integer(record.get("year"), "Release year")
        genre_name = require_text(record.get("genre"), "Genre")
        description = record.get("description", "")

        if not isinstance(description, str):
            raise ValueError("Description must be text.")

        if record.get("type") == "film":
            minutes = require_integer(record.get("minutes"), "Duration")
            title = Film(name, year, minutes)

        elif record.get("type") == "show":
            network = require_text(record.get("network"), "Network")
            title = TVShow(name, year, network)
            seen_seasons = set()

            for season_data in require_list(
                record.get("seasons"), "Seasons"
            ):
                if not isinstance(season_data, dict):
                    raise ValueError("Invalid season.")

                number = require_integer(
                    season_data.get("number"), "Season number"
                )
                if number in seen_seasons:
                    raise ValueError("Duplicate season number.")
                seen_seasons.add(number)

                season = Season(number)

                for episode_data in require_list(
                    season_data.get("episodes"), "Episodes"
                ):
                    if not isinstance(episode_data, dict):
                        raise ValueError("Invalid episode.")

                    episode_name = require_text(
                        episode_data.get("name"), "Episode title"
                    )
                    seconds = require_integer(
                        episode_data.get("seconds"), "Episode duration"
                    )
                    season.add_episode(Episode(episode_name, seconds))

                title.add_season(season)
        else:
            raise ValueError("Title type must be film or show.")

        for actor_name in require_list(record.get("actors"), "Actors"):
            require_text(actor_name, "Actor name")
            if actor_name not in actors:
                actors[actor_name] = Actor(actor_name)
            title.link_actor(actors[actor_name])

        if genre_name not in genres:
            genres[genre_name] = Genre(genre_name)

        genre = genres[genre_name]
        genre.register_title(title)

        entries.append({
            "id": title_id,
            "title": title,
            "genre": genre,
            "description": description,
        })

    return entries


def load_catalog(path=CATALOG_FILE):
    try:
        with Path(path).open("r", encoding="utf-8") as file:
            records = json.load(file)
    except FileNotFoundError:
        return build_catalog()

    return records_to_catalog(records)


def save_catalog(entries, path=CATALOG_FILE):
    records = catalog_to_records(entries)
    records_to_catalog(records)  # Validate before changing the saved file.

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
            json.dump(records, file, ensure_ascii=False, indent=2)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)