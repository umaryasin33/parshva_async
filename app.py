import pandas as pd
from flask import Flask, render_template, jsonify
import json
from urllib.parse import unquote
import re



app = Flask(__name__)


def read_excel():
    df = pd.read_excel('./export29913.xlsx')
    columns_to_ffill = ['Supplier', 'PO Number.2']
    df[columns_to_ffill] = df[columns_to_ffill].ffill()
    return df   

@app.route('/')
def index():
    df = read_excel()

    suppliers = list(sorted(set(df['Supplier'])))
    return render_template('index.html', suppliers=suppliers)


@app.route('/get_purchase_orders/<supplier>')
def get_purchase_orders(supplier):
    df = read_excel()

    purchase_orders = df[df['Supplier'] == supplier]['PO Number.2'].drop_duplicates().tolist()

    return jsonify(purchase_orders)

@app.route('/get_description/<order_number>')
def get_description(order_number):
    df = read_excel()
    print(order_number)
    order_number = re.sub(r'^(\d{4})', r'\1/', order_number)

    descriptions = df[df['PO Number.2'] == order_number]['Description'].tolist()
    return jsonify({'descriptions': descriptions})

if __name__ == '__main__':
    app.run(debug=True)