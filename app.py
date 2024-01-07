from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

products = [
    {"id": 1, "name": "23+24-周末票", "price": 500},
    {"id": 2, "name": "23-全天票", "price": 300},
    {"id": 3, "name": "24-全天票", "price": 300},
    {"id": 4, "name": "23-夜場票", "price": 180},
    {"id": 5, "name": "24-夜場票", "price": 180},
]

@app.route("/")
def index():
    return render_template("mainpage.html", products=products)

@app.route("/buy", methods=["POST"])
def buy_tickets():
    ticket_id = request.form.get("ticket_id")
    quantity = int(request.form.get("quantity"))

    ticket_info = next(
        (product for product in products if str(product["id"]) == ticket_id), None
    )
    if ticket_info:
        total_price = ticket_info["price"] * quantity
        session["ticket_info"] = ticket_info
        session["quantity"] = quantity
        session["total_price"] = total_price

        return redirect(url_for("payment_success"))
    else:
        return "Invalid ticket selection", 400

@app.route("/payment_success")
def payment_success():
    ticket_info = session.get("ticket_info")
    quantity = session.get("quantity")
    total_price = session.get("total_price")

    return render_template(
        "payment_success.html",
        ticket_type=ticket_info["name"],
        quantity=quantity,
        total_price=total_price,
    )

if __name__ == "__main__":
    app.run(debug=True)
