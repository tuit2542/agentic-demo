from flask import Flask, jsonify, redirect, request

from src.store import UrlStore


def create_app():
    app = Flask(__name__)
    store = UrlStore()

    @app.post("/shorten")
    def shorten():
        data = request.get_json(silent=True) or {}
        url = data.get("url")
        if not url:
            return jsonify({"error": "url is required"}), 400
        sid = store.shorten(url)
        return jsonify({"short_id": sid}), 201

    @app.get("/<sid>")
    def redirect_url(sid):
        url = store.resolve(sid)
        if url is None:
            return jsonify({"error": "not found"}), 404
        return redirect(url)

    @app.get("/stats/<sid>")
    def stats(sid):
        clicks = store.stats(sid)
        return jsonify({"short_id": sid, "clicks": clicks})

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
