"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        pinned = sorted(
            [(i, n) for i, n in enumerate(app.notes) if n.get("pinned")],
            key=lambda pair: pair[1]["pinned_order"]
        )
        unpinned = [(i, n) for i, n in enumerate(app.notes) if not n.get("pinned")]
        return render_template("home.html", note_pairs=pinned + unpinned)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            errors = {}

            if not title:
                errors["title"] = "Title is required"
            if not body:
                errors["body"] = "Body is required"

            raw_tags = (request.form.get("tags") or "").strip()
            tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

            if errors:
                return render_template("new_note.html", title=title, body=body, tags=raw_tags, errors=errors)

            app.notes.append({"title": title, "body": body, "tags": tags, "pinned": False, "pinned_order": None})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    @app.route("/notes/<int:note_id>/pin", methods=["POST"])
    def pin_note(note_id):
        if 0 <= note_id < len(app.notes):
            note = app.notes[note_id]
            if note.get("pinned"):
                note["pinned"] = False
                note["pinned_order"] = None
            else:
                note["pinned"] = True
                note["pinned_order"] = datetime.now()
        return redirect(url_for("home"))

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
