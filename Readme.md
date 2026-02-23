# FakeDonald's Inventory Management - Web App

A Flask web application that takes the original command-line inventory tool and turns it into something you can actually hand to a staff member. Built for a burger shop, but the logic works for any small operation tracking boxed goods.

This is the second version of the project. The first version was a Python terminal script. This one keeps all that same backend logic and wraps it in a proper browser interface, plus adds a machine learning prediction feature for next-day inventory needs.

---

## Features

- **Dashboard with live alerts** - Opens straight to your inventory with highlighted warnings for anything below its critical stock level
- **Daily inventory entry** - Form-based input to update box counts at the start of each shift
- **Order placement** - Select items, enter quantities, get a full order summary with subtotal, GST (5%), and total
- **Waste logging** - Log units wasted per item; the app calculates total dollar value lost and saves it to a usage log
- **Inventory prediction** - Uses a linear regression model trained on your `usage_log.csv` to estimate what you'll need tomorrow

---

## Tech Stack

| Layer | Tool |
|---|---|
| Backend | Python 3, Flask |
| Templates | Jinja2 (HTML) |
| Styling | Custom CSS |
| Data | CSV files |
| ML | scikit-learn (LinearRegression) |
| Data handling | pandas |

---

## Getting Started

### 1. Install dependencies

```bash
pip install flask pandas scikit-learn
```

Or if a `requirements.txt` is included:

```bash
pip install -r requirements.txt
```

### 2. Make sure your CSV files are in place

- `inventory.csv` - your main stock data (required)
- `usage_log.csv` - daily waste data used for predictions (required for the predict page, can start empty with a header row)

`inventory.csv` format:
```
name,quantity,price,units_per_box,critical_level
burger bun,5,7.85,144,2
```

`usage_log.csv` format:
```
date,name,units_used
2025-06-10,burger bun,12
```

### 3. Start the app

```bash
python app.py
```

### 4. Open in your browser

```
http://127.0.0.1:5000
```

---

## Project Structure

```
Assignment 2/
├── app.py                              # Flask routes and app logic
├── mcd_inventory_critical_threshold.py # Core inventory functions (load, save, etc.)
├── predictor.py                        # ML prediction module
├── inventory.csv                       # Main inventory data
├── usage_log.csv                       # Usage history for predictions
│
├── templates/
│   ├── base.html                       # Shared layout
│   ├── index.html                      # Dashboard / home
│   ├── inventory.html                  # Full inventory table
│   ├── entry.html                      # Daily stock entry form
│   ├── order.html                      # Order form + receipt
│   ├── waste.html                      # Waste logging form
│   └── predict.html                    # Prediction results
│
└── static/
    ├── style.css                       # App styling
    └── mcdonalds-15-logo-png-transparent.png
```

---

## How the Prediction Works

Every time waste is logged through the web app, a row gets written to `usage_log.csv` with today's date, the item name, and units used. The prediction page reads that file, runs a simple linear regression per item (fitting usage against day number), and projects what tomorrow's usage will look like.

It needs at least 2 data points per item to generate a prediction - anything with less will show "Insufficient data."

---

## Pages Overview

| Route | What it does |
|---|---|
| `/` | Home dashboard with low stock alerts |
| `/inventory` | Full inventory table |
| `/entry` | Update current box counts |
| `/order` | Place a supply order |
| `/waste` | Log wasted units |
| `/predict` | View ML-based next-day predictions |

---
<img width="1855" height="904" alt="image" src="https://github.com/user-attachments/assets/ec539cb9-ae6f-480e-8e5b-3fb4ac975ef0" />


## Author

Aayush Patel  
Assignment 2 - Flask Application for Business Problem Solving  
University of Lethbridge
