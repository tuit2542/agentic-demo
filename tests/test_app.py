from src.app import create_app


def test_shorten_returns_201():
    app = create_app()
    resp = app.test_client().post("/shorten", json={"url": "https://example.com"})
    assert resp.status_code == 201
    assert "short_id" in resp.json


def test_redirect_moves_to_original():
    app = create_app()
    resp = app.test_client().post("/shorten", json={"url": "https://example.com"})
    sid = resp.json["short_id"]
    resp2 = app.test_client().get(f"/{sid}", follow_redirects=False)
    assert resp2.status_code == 302
    assert resp2.headers["Location"] == "https://example.com"


def test_stats_returns_count():
    app = create_app()
    client = app.test_client()
    sid = client.post("/shorten", json={"url": "https://example.com"}).json["short_id"]
    client.get(f"/{sid}")
    client.get(f"/{sid}")
    resp = client.get(f"/stats/{sid}")
    assert resp.status_code == 200
    assert resp.json["clicks"] == 2


def test_shorten_missing_url_returns_400():
    app = create_app()
    resp = app.test_client().post("/shorten", json={})
    assert resp.status_code == 400


def test_redirect_unknown_returns_404():
    app = create_app()
    resp = app.test_client().get("/zzzzzz")
    assert resp.status_code == 404
