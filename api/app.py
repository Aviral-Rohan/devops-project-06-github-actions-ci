from flask import Flask, jsonify, request

from pricing import MENU, PricingError, quote

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok", service="api")


@app.get("/menu")
def menu():
    return jsonify([{"id": k, **v} for k, v in MENU.items()])


@app.post("/quote")
def get_quote():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify(quote(data.get("items", []), data.get("coupon")))
    except PricingError as err:
        return jsonify(error=str(err)), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
