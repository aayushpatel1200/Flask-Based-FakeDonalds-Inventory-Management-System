# FakeDonald's Inventory Management System

## Overview
This is a Flask-based web application designed to help a burger shop manage its inventory efficiently. The application allows staff to view current stock, update daily inventory, place orders (with GST included), log waste, and predict future inventory needs using recent usage data and a basic machine learning model.

This project is an upgrade of a previous command-line inventory system. The original Python logic was preserved and integrated into a web-based solution with an improved user interface.

---

## Features
- View inventory with low-stock alerts
- Daily inventory entry for current stock updates
- Place supply orders for multiple products at once
- Auto-calculation of subtotal, GST, and total cost
- Log wasted products and calculate total waste cost
- Predict next day’s inventory needs using machine learning
- Clean, responsive web UI using HTML, CSS, and Flask

---

## Technologies Used
- Python 3
- Flask
- Jinja2 (HTML templates)
- Pandas (for data handling)
- scikit-learn (for regression-based predictions)
- CSV files (used as the data source)

---

## How to Run This App

### 1. Install Dependencies
Open a terminal in the project folder and run:
pip install flask pandas scikit-learn


### 2. Start the Flask Application
python app.py


### 3. Open in Your Web Browser
Visit:
http://127.0.0.1:5000


---

## Folder Structure
Assignment 2/
├── app.py # Main Flask app
├── mcd_inventory_critical_threshold.py # Original inventory logic (unchanged)
├── predictor.py # Prediction module (ML)
├── inventory.csv # Main inventory database
├── usage_log.csv # Daily usage data for prediction
│
├── /templates/ # HTML templates
│ ├── base.html
│ ├── index.html
│ ├── inventory.html
│ ├── entry.html
│ ├── order.html
│ ├── waste.html
│ └── predict.html
│
├── /static/
│ ├── style.css # Custom styles
│ └── mcdonalds-logo.png # Optional logo in UI

---

## Author
Aayush patel  
Assignment 2 – Flask Application for Business Problem Solving  
University of Lethbridge