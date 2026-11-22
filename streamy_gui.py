"""Streamy desktop catalog interface."""

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from streamy_catalog import build_catalog, duration_minutes
from streamy_core import Film


class StreamyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Streamy | Personal Media Library")
        self.geometry("1050x680")
        self.minsize(800, 550)

        self.catalog = build_catalog()
        self.entries_by_id = {
            entry["id"]: entry for entry in self.catalog
        }

        self.search_var = tk.StringVar()
        self.genre_var = tk.StringVar(value="All genres")
        self.status_var = tk.StringVar()

        self.create_widgets()

        self.search_var.trace_add("write", self.refresh_catalog)
        self.genre_var.trace_add("write", self.refresh_catalog)

        self.refresh_catalog()

    def create_widgets(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=32)
        style.configure(
            "Title.TLabel",
            font=("TkDefaultFont", 24, "bold"),
        )

        main = ttk.Frame(self, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="STREAMY",
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            main,
            text="Discover stories. Build your personal media library.",
        ).pack(anchor="w", pady=(0, 18))

        filters = ttk.Frame(main)
        filters.pack(fill="x", pady=(0, 15))

        ttk.Label(filters, text="Search:").pack(side="left")

        search = ttk.Entry(
            filters,
            textvariable=self.search_var,
            width=35,
        )
        search.pack(side="left", fill="x", expand=True, padx=(8, 18))

        ttk.Label(filters, text="Genre:").pack(side="left")

        genres = sorted({
            entry["genre"].genre_name for entry in self.catalog
        })

        ttk.Combobox(
            filters,
            textvariable=self.genre_var,
            values=["All genres", *genres],
            state="readonly",
            width=18,
        ).pack(side="left", padx=(8, 0))

        content = ttk.Frame(main)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        catalog_frame = ttk.LabelFrame(
            content,
            text="Catalog",
            padding=10,
        )
        catalog_frame.grid(
            row=0, column=0, sticky="nsew", padx=(0, 12)
        )
        catalog_frame.columnconfigure(0, weight=1)
        catalog_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            catalog_frame,
            columns=("name", "year", "type"),
            show="headings",
            selectmode="browse",
        )

        for column, heading, width in (
            ("name", "Title", 220),
            ("year", "Year", 60),
            ("type", "Type", 80),
        ):
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=width, minwidth=50)

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            catalog_frame,
            orient="vertical",
            command=self.tree.yview,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<<TreeviewSelect>>", self.show_details)

        details_frame = ttk.LabelFrame(
            content,
            text="Title details",
            padding=10,
        )
        details_frame.grid(row=0, column=1, sticky="nsew")

        self.details = ScrolledText(
            details_frame,
            wrap="word",
            width=32,
            font=("TkDefaultFont", 11),
            padx=12,
            pady=12,
            state="disabled",
        )
        self.details.pack(fill="both", expand=True)

        ttk.Label(
            main,
            textvariable=self.status_var,
        ).pack(anchor="w", pady=(12, 0))

        search.focus_set()

    def refresh_catalog(self, *_):
        previous_selection = self.tree.selection()
        query = self.search_var.get().strip().casefold()
        genre = self.genre_var.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for entry in self.catalog:
            title = entry["title"]

            if query not in title.name.casefold():
                continue

            if (
                genre != "All genres"
                and entry["genre"].genre_name != genre
            ):
                continue

            media_type = "Film" if isinstance(title, Film) else "TV Show"

            self.tree.insert(
                "",
                "end",
                iid=entry["id"],
                values=(title.name, title.release_year, media_type),
            )

        visible = self.tree.get_children()
        self.status_var.set(
            f"{len(visible)} of {len(self.catalog)} titles displayed"
            " | Demo catalog"
        )

        if visible:
            selected = (
                previous_selection[0]
                if previous_selection and previous_selection[0] in visible
                else visible[0]
            )
            self.tree.selection_set(selected)
            self.tree.focus(selected)
            self.tree.see(selected)
            self.show_details()
        else:
            self.set_details(
                "No matching titles.\n\nTry another search or genre."
            )

    def set_details(self, text):
        self.details.configure(state="normal")
        self.details.delete("1.0", tk.END)
        self.details.insert("1.0", text)
        self.details.configure(state="disabled")

    def show_details(self, _event=None):
        selection = self.tree.selection()
        if not selection:
            return

        entry = self.entries_by_id[selection[0]]
        title = entry["title"]
        media_type = "Film" if isinstance(title, Film) else "TV Show"

        lines = [
            title.name,
            f"{title.release_year} | {media_type}",
            f"Genre: {entry['genre'].genre_name}",
            f"Catalog duration: {duration_minutes(title):g} minutes",
            "",
            entry["description"],
            "",
            "Cast:",
            ", ".join(actor.full_name for actor in title.cast_actors),
        ]

        if not isinstance(title, Film):
            lines.extend(["", f"Network: {title.network}", "", "Episodes:"])

            for season in title.seasons:
                lines.append(f"\nSeason {season.season_number}")

                for episode in season.episodes:
                    minutes = episode.duration_seconds / 60
                    lines.append(
                        f"  • {episode.episode_title} ({minutes:g} min)"
                    )

        self.set_details("\n".join(lines))


if __name__ == "__main__":
    app = StreamyApp()
    app.mainloop()