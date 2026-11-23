"""Streamy personal library: watchlist, reviews and watched statistics."""

from copy import deepcopy
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from streamy_gui import StreamyApp
from streamy_catalog import duration_minutes
from streamy_storage import DATA_FILE, load_library, save_library

from streamy_catalog_editor import CatalogEditor
from streamy_catalog_store import (
    catalog_to_records,
    records_to_catalog,
    save_catalog,
)


class PersonalStreamyApp(StreamyApp):
    def __init__(self):
        self.library = load_library()
        super().__init__()
        self.title("Streamy | Personal Library")
        self.sync_reviews()
        self.refresh_catalog()

    def create_widgets(self):
        super().create_widgets()

        # Insert personal-library controls above the catalog/details area.
        content = self.tree.master.master
        main = content.master

        controls = ttk.LabelFrame(
            main, text="My library", padding=10
        )
        controls.pack(fill="x", pady=(0, 12), before=content)

        actions = [
            ("Add title", self.add_title),
            ("Edit title", self.edit_title),
            ("Toggle watchlist", self.toggle_watchlist),
            ("Mark watched / unwatched", self.toggle_watched),
            ("Write / edit review", self.edit_review),
            ("Show my watchlist", self.show_watchlist),
            ("Playback demo", self.playback_demo),
        ]

        for index, (label, command) in enumerate(actions):
            row, column = divmod(index, 3)
            ttk.Button(
                controls,
                text=label,
                command=command,
            ).grid(
                row=row,
                column=column,
                sticky="ew",
                padx=4,
                pady=4,
            )

        for column in range(3):
            controls.columnconfigure(column, weight=1)

        self.stats_var = tk.StringVar()
        ttk.Label(
            controls,
            textvariable=self.stats_var,
            wraplength=700,
        ).grid(
            row=3, column=0, columnspan=3,
            sticky="w", padx=4, pady=(8, 0),
        )
    def add_title(self):
        CatalogEditor(self, on_save=self.save_title_record)

    def edit_title(self):
        entry = self.selected_entry()
        if entry is None:
            return

        record = catalog_to_records([entry])[0]
        CatalogEditor(
            self,
            on_save=self.save_title_record,
            record=record,
        )

    def save_title_record(self, record):
        records = catalog_to_records(self.catalog)

        for index, existing in enumerate(records):
            if existing["id"] == record["id"]:
                records[index] = record
                break
        else:
            records.append(record)

        updated = records_to_catalog(records)

        # Save first; keep the current catalog if writing fails.
        save_catalog(updated)

        self.catalog = updated
        self.entries_by_id = {
            entry["id"]: entry for entry in self.catalog
        }
        self.sync_reviews()

        genres = sorted({
            entry["genre"].genre_name for entry in self.catalog
        })
        self.genre_box.configure(values=["All genres", *genres])

        self.search_var.set("")
        self.genre_var.set("All genres")
        self.view_var.set("All titles")
        self.refresh_catalog()

        self.tree.selection_set(record["id"])
        self.tree.focus(record["id"])
        self.tree.see(record["id"])
        self.show_details()


    def selected_entry(self):
        selection = self.tree.selection()

        if not selection:
            messagebox.showinfo(
                "Select a title",
                "Please select a title from the catalog.",
                parent=self,
            )
            return None

        return self.entries_by_id[selection[0]]

    def sync_reviews(self):
        """Restore personal reviews into the existing domain objects."""
        for entry in self.catalog:
            title = entry["title"]
            title.reviews.clear()
            review = self.library["reviews"].get(entry["id"])

            if review:
                title.add_review(review["rating"], review["text"])

    def commit_library(self, updated):
        """Update the interface only after saving succeeds."""
        try:
            save_library(updated)
        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Could not save",
                f"Your change was not saved.\n\n{error}",
                parent=self,
            )
            return False

        self.library = updated
        self.sync_reviews()
        self.refresh_catalog()
        return True

    def toggle_membership(self, field):
        entry = self.selected_entry()
        if entry is None:
            return

        updated = deepcopy(self.library)
        title_id = entry["id"]

        if title_id in updated[field]:
            updated[field].remove(title_id)
        else:
            updated[field].append(title_id)

        self.commit_library(updated)

    def toggle_watchlist(self):
        self.toggle_membership("watchlist")

    def toggle_watched(self):
        self.toggle_membership("watched")

    def edit_review(self):
        entry = self.selected_entry()
        if entry is None:
            return

        existing = self.library["reviews"].get(entry["id"], {})

        rating = simpledialog.askinteger(
            "Your rating",
            f"Rate {entry['title'].name} from 1 to 5:",
            initialvalue=existing.get("rating", 5),
            minvalue=1,
            maxvalue=5,
            parent=self,
        )
        if rating is None:
            return

        text = simpledialog.askstring(
            "Your review",
            "Write a short review:",
            initialvalue=existing.get("text", ""),
            parent=self,
        )
        if text is None:
            return

        if not text.strip():
            messagebox.showwarning(
                "Empty review",
                "Please enter some review text.",
                parent=self,
            )
            return

        updated = deepcopy(self.library)
        updated["reviews"][entry["id"]] = {
            "rating": rating,
            "text": text.strip(),
        }

        self.commit_library(updated)

    def show_watchlist(self):
        titles = [
            entry["title"].name
            for entry in self.catalog
            if entry["id"] in self.library["watchlist"]
        ]

        messagebox.showinfo(
            "My watchlist",
            "\n".join(f"• {name}" for name in titles)
            if titles else "Your watchlist is empty.",
            parent=self,
        )

    def playback_demo(self):
        entry = self.selected_entry()
        if entry is None:
            return

        # This calls the lab's simulated playback method.
        success = entry["title"].play_media("DEMO_TOKEN")

        messagebox.showinfo(
            "Playback simulation",
            (
                "Demo authorization succeeded.\n\n"
                "This is the laboratory playback simulation; "
                "no video is streamed and no viewing time is recorded."
                if success else "Demo authorization failed."
            ),
            parent=self,
        )

    def refresh_catalog(self, *_):
        super().refresh_catalog()

        known_ids = set(self.entries_by_id)
        watched = known_ids.intersection(self.library["watched"])
        watchlist = known_ids.intersection(self.library["watchlist"])

        minutes = sum(
            duration_minutes(self.entries_by_id[title_id]["title"])
            for title_id in watched
        )

        self.stats_var.set(
            f"Watchlist: {len(watchlist)}  |  "
            f"Marked watched: {len(watched)}  |  "
            f"Marked-watched catalog duration: {minutes:g} min"
        )

    def show_details(self, _event=None):
        super().show_details(_event)

        selection = self.tree.selection()
        if not selection:
            return

        title_id = selection[0]
        watchlisted = title_id in self.library["watchlist"]
        watched = title_id in self.library["watched"]

        extra = (
            "\n\nMY LIBRARY\n"
            f"Watchlist: {'Yes' if watchlisted else 'No'}\n"
            f"Watched: {'Yes' if watched else 'No'}"
        )

        review = self.library["reviews"].get(title_id)
        if review:
            extra += (
                f"\n\nMy rating: {review['rating']}/5\n"
                f"My review: {review['text']}"
            )
        else:
            extra += "\n\nNo personal review yet."

        self.details.configure(state="normal")
        self.details.insert(tk.END, extra)
        self.details.configure(state="disabled")


if __name__ == "__main__":
    try:
        app = PersonalStreamyApp()
    except (OSError, ValueError) as error:
        error_window = tk.Tk()
        error_window.withdraw()
        messagebox.showerror(
            "Cannot open personal library",
            f"Could not load catalog or personal library data.\n\n{error}\n\n"
            "The existing file has not been overwritten.",
            parent=error_window,
        )
        error_window.destroy()
    else:
        app.mainloop()