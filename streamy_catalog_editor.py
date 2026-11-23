"""Add/edit dialog for Streamy catalog entries."""

from copy import deepcopy
from uuid import uuid4
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from streamy_catalog_store import records_to_catalog


class CatalogEditor(simpledialog.Dialog):
    def __init__(self, parent, on_save, record=None):
        self.record = deepcopy(record)
        self.on_save = on_save
        self.title_id = record["id"] if record else f"title-{uuid4().hex}"

        super().__init__(
            parent,
            title="Edit title" if record else "Add title",
        )

    def body(self, master):
        record = self.record or {}
        self.fields = {}

        labels = [
            ("name", "Title", record.get("name", "")),
            ("year", "Release year", record.get("year", "")),
            ("genre", "Genre", record.get("genre", "")),
            ("actors", "Actors (comma separated)",
             ", ".join(record.get("actors", []))),
            ("minutes", "Film duration (whole minutes)",
             record.get("minutes", "")),
            ("network", "TV show network",
             record.get("network", "")),
        ]

        ttk.Label(master, text="Type").grid(
            row=0, column=0, sticky="w", padx=8, pady=6
        )
        self.type_var = tk.StringVar(value=record.get("type", "film"))
        self.type_box = ttk.Combobox(
            master,
            textvariable=self.type_var,
            values=("film", "show"),
            state="disabled" if self.record else "readonly",
            width=38,
        )
        self.type_box.grid(row=0, column=1, sticky="ew", padx=8, pady=6)
        self.type_box.bind("<<ComboboxSelected>>", self.update_fields)

        for row, (key, label, value) in enumerate(labels, start=1):
            ttk.Label(master, text=label).grid(
                row=row, column=0, sticky="w", padx=8, pady=6
            )
            field = ttk.Entry(master, width=42)
            field.insert(0, str(value))
            field.grid(row=row, column=1, sticky="ew", padx=8, pady=6)
            self.fields[key] = field

        ttk.Label(master, text="Description").grid(
            row=7, column=0, sticky="nw", padx=8, pady=6
        )
        self.description = tk.Text(master, width=42, height=5, wrap="word")
        self.description.insert("1.0", record.get("description", ""))
        self.description.grid(
            row=7, column=1, sticky="ew", padx=8, pady=6
        )

        ttk.Label(
            master,
            text=(
                "Existing seasons and episodes are preserved.\n"
                "New TV shows start without episodes."
            ),
            wraplength=440,
        ).grid(row=8, column=0, columnspan=2, padx=8, pady=10)

        master.columnconfigure(1, weight=1)
        self.update_fields()
        return self.fields["name"]

    def update_fields(self, _event=None):
        is_film = self.type_var.get() == "film"
        self.fields["minutes"].configure(
            state="normal" if is_film else "disabled"
        )
        self.fields["network"].configure(
            state="disabled" if is_film else "normal"
        )

    def validate(self):
        try:
            record = deepcopy(self.record) if self.record else {}
            record.update({
                "id": self.title_id,
                "type": self.type_var.get(),
                "name": self.fields["name"].get().strip(),
                "genre": self.fields["genre"].get().strip(),
                "description": self.description.get(
                    "1.0", "end-1c"
                ).strip(),
                "actors": list(dict.fromkeys(
                    name.strip()
                    for name in self.fields["actors"].get().split(",")
                    if name.strip()
                )),
            })

            try:
                record["year"] = int(self.fields["year"].get())
            except ValueError:
                raise ValueError("Release year must be a whole number.")

            if record["type"] == "film":
                try:
                    record["minutes"] = int(
                        self.fields["minutes"].get()
                    )
                except ValueError:
                    raise ValueError(
                        "Film duration must be a whole number."
                    )
            else:
                record["network"] = self.fields["network"].get().strip()
                record.setdefault("seasons", [])

            records_to_catalog([record])

        except ValueError as error:
            messagebox.showerror("Invalid entry", str(error), parent=self)
            return False

        # Keep the form open if saving fails.
        try:
            self.on_save(record)
        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Could not save",
                str(error),
                parent=self,
            )
            return False

        return True