from flask import Flask, request, jsonify, render_template
import sqlite3
import re

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mock_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product TEXT,
                        amount INTEGER,
                        region TEXT
                    )''')
    cursor.executemany('''INSERT INTO sales (product, amount, region) VALUES (?, ?, ?)''',
                       [('Laptop', 1500, 'North'), ('Phone', 800, 'South'), ('Tablet', 1200, 'East')])
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    natural_query = data.get('query', '')
    sql_query = convert_to_sql(natural_query)
    
    if not sql_query:
        return jsonify({"error": "Unable to process query"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()
        return jsonify({"query": sql_query, "result": [dict(row) for row in result]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/explain', methods=['POST'])
def explain():
    data = request.json
    natural_query = data.get('query', '')
    sql_query = convert_to_sql(natural_query)
    return jsonify({"natural_query": natural_query, "sql_query": sql_query})

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    natural_query = data.get('query', '')
    sql_query = convert_to_sql(natural_query)
    
    if sql_query:
        return jsonify({"valid": True, "sql_query": sql_query})
    else:
        return jsonify({"valid": False, "message": "Invalid query"})

def convert_to_sql(natural_query):
    natural_query = natural_query.lower()
    patterns = {
        r'how many sales': "SELECT COUNT(*) as sales_count FROM sales;",
        r'total sales amount': "SELECT SUM(amount) as total_sales FROM sales;",
        r'sales by region': "SELECT region, SUM(amount) as total FROM sales GROUP BY region;"
    }
    for pattern, sql in patterns.items():
        if re.search(pattern, natural_query):
            return sql
    return None

if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)
