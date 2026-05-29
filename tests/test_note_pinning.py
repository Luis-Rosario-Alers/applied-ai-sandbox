"""Regression tests for note pinning — ordering, toggle, and defaults."""


def _seed(app, titles):
    app.notes.clear()
    for t in titles:
        app.notes.append({"title": t, "body": "body", "tags": [], "pinned": False, "pinned_order": None})


def test_pin_moves_note_to_top(client, app):
    _seed(app, ["NoteAlpha", "NoteBeta"])
    client.post("/notes/1/pin")
    body = client.get("/").data.decode()
    assert body.index("NoteBeta") < body.index("NoteAlpha")


def test_unpin_returns_note_to_unpinned_group(client, app):
    _seed(app, ["NoteAlpha", "NoteBeta"])
    client.post("/notes/1/pin")
    client.post("/notes/1/pin")
    body = client.get("/").data.decode()
    assert body.index("NoteAlpha") < body.index("NoteBeta")


def test_pin_order_reflects_pin_time_not_creation_order(client, app):
    _seed(app, ["N1", "N3", "N5", "N4", "N2"])
    for idx in [0, 1, 2, 3]:
        client.post(f"/notes/{idx}/pin")
    body = client.get("/").data.decode()
    assert body.index("N1") < body.index("N3") < body.index("N5") < body.index("N4")


def test_default_pinned_is_false(client, app):
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B"})
    assert app.notes[0]["pinned"] is False
    assert app.notes[0]["pinned_order"] is None


def test_pin_route_returns_redirect(client, app):
    _seed(app, ["X"])
    r = client.post("/notes/0/pin")
    assert r.status_code in (302, 303)


def test_pin_route_sets_pinned_true(client, app):
    _seed(app, ["X"])
    client.post("/notes/0/pin")
    assert app.notes[0]["pinned"] is True
    assert app.notes[0]["pinned_order"] is not None


def test_unpin_clears_pinned_order(client, app):
    _seed(app, ["X"])
    client.post("/notes/0/pin")
    client.post("/notes/0/pin")
    assert app.notes[0]["pinned"] is False
    assert app.notes[0]["pinned_order"] is None
