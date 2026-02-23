from flask import Flask, render_template, request, redirect
import mcd_inventory_critical_threshold as mcd
from datetime import date

app = Flask(__name__)
filename = 'inventory.csv'

# Load inventory from the CSV using the existing logic
def get_inventory():
    return mcd.load_inventory(filename)

@app.route("/")
def home():
    inventory = get_inventory()
    low_stock = {
        name: item
        for name, item in inventory.items()
        if item['quantity'] < item['critical_level']
    }
    return render_template("index.html", inventory=inventory, low_stock=low_stock)


@app.route("/inventory")
def view_inventory():
    inventory = get_inventory()
    return render_template("inventory.html", inventory=inventory)

@app.route("/entry", methods=["GET", "POST"])
def daily_entry():
    inventory = get_inventory()
    if request.method == "POST":
        for name in inventory:
            if name in request.form:
                try:
                    inventory[name]['quantity'] = int(request.form[name])
                except:
                    pass
        mcd.save_inventory(inventory, filename)
        return redirect("/inventory")
    return render_template("entry.html", inventory=inventory)

@app.route("/order", methods=["GET", "POST"])
def place_order():
    inventory = get_inventory()
    order_summary = []
    total = 0

    if request.method == "POST":
        for name in inventory:
            try:
                qty = int(request.form.get(name, 0))
                if qty > 0:
                    item = inventory[name]
                    subtotal = qty * item['price']
                    order_summary.append({
                        "name": name.title(),
                        "qty": qty,
                        "unit_price": item['price'],
                        "subtotal": subtotal
                    })
                    inventory[name]['quantity'] += qty
                    total += subtotal
            except:
                continue

        mcd.save_inventory(inventory, filename)

        gst = round(total * 0.05, 2)
        grand_total = round(total + gst, 2)

        return render_template("order.html", inventory=inventory, submitted=True,
                               order_summary=order_summary, total=total,
                               gst=gst, grand_total=grand_total)

    return render_template("order.html", inventory=inventory, submitted=False)


@app.route("/waste", methods=["GET", "POST"])
def waste_log():
    inventory = get_inventory()
    total_waste = 0
    if request.method == "POST":
        with open('usage_log.csv', 'a') as log_file:
            for name in inventory:
                try:
                    wasted = int(request.form.get(name, 0))
                    total_waste += wasted * inventory[name]['per_unit_price']
                    
                    log_file.write(f"{date.today()},{name},{wasted}\n")
                except:
                    pass
        return render_template("waste.html", inventory=inventory, total_waste=total_waste, done=True)
    return render_template("waste.html", inventory=inventory, done=False)

@app.route("/predict")
def predict():
    from predictor import predict_inventory
    predictions = predict_inventory()
    return render_template("predict.html", predictions=predictions)

if __name__ == "__main__":
    app.run(debug=True)
