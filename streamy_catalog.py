"""Sample catalog for the Streamy desktop application."""

from streamy_core import Actor, Episode, Film, Genre, Season, TVShow


def build_catalog():
    """Build fresh domain objects and return entries with stable IDs."""
    genres = {
        name: Genre(name)
        for name in ("Sci-Fi", "Adventure", "Drama")
    }

    actor_one = Actor("Alex Morgan")
    actor_two = Actor("Sam Taylor")

    entries = []

    def register(entry_id, title, genre_name, description):
        genres[genre_name].register_title(title)
        title.link_actor(actor_one)
        title.link_actor(actor_two)

        entries.append({
            "id": entry_id,
            "title": title,
            "genre": genres[genre_name],
            "description": description,
        })

    register(
        "film-orbit",
        Film("Beyond Orbit", 2026, 112),
        "Sci-Fi",
        "A young engineer discovers a mysterious signal from deep space.",
    )

    register(
        "film-island",
        Film("The Hidden Island", 2025, 98),
        "Adventure",
        "Two friends follow an old map to an island full of secrets.",
    )

    register(
        "film-last-letter",
        Film("The Last Letter", 2024, 105),
        "Drama",
        "An unexpected letter brings a separated family together.",
    )

    show = TVShow("Neon City", 2026, "Streamy Demo")
    season = Season(1)
    season.add_episode(Episode("The Signal", 42 * 60))
    season.add_episode(Episode("The Search", 45 * 60))
    season.add_episode(Episode("The Discovery", 48 * 60))
    show.add_season(season)

    register(
        "show-neon-city",
        show,
        "Sci-Fi",
        "A detective investigates strange events in a futuristic city.",
    )

    show = TVShow("Mountain Trails", 2025, "Streamy Demo")
    season = Season(1)
    season.add_episode(Episode("First Steps", 35 * 60))
    season.add_episode(Episode("The Summit", 40 * 60))
    show.add_season(season)

    register(
        "show-mountain-trails",
        show,
        "Adventure",
        "A group of explorers attempts a difficult mountain expedition.",
    )

    return entries


def duration_minutes(title):
    """Return film duration or the total duration of cataloged episodes."""
    if isinstance(title, Film):
        return title.length_minutes

    seconds = sum(
        episode.duration_seconds
        for season in title.seasons
        for episode in season.episodes
    )
    return seconds / 60


if __name__ == "__main__":
    for entry in build_catalog():
        title = entry["title"]
        print(
            f"{title.name} | {entry['genre'].genre_name} | "
            f"{duration_minutes(title):g} min"
        )