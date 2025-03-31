Gen AI Query Engine

A lightweight backend service that simulates AI-powered data query processing, allowing users to input natural language queries and receive structured SQL responses.

Features

Convert natural language queries into SQL

Execute SQL on a mock database

Validate and explain queries

Lightweight authentication

 Folder Structure
/genai_query_engine
│── app.py               # Main Flask API
│── mock_db.sqlite       # SQLite Database (generated at runtime)
│── requirements.txt     # Dependencies
│── README.md            # Project Documentation
│── app.py                
│── static/
│   ├── style.css
│── templates/
│   ├── index.html


Setup Instructions

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/genai_query_engine.git
cd genai_query_engine

2. Install Dependencies
pip install -r requirements.txt

3.  Run the Flask Server
python app.py

4. Access the Frontend
Open http://127.0.0.1:5000 in your browser.

 API Endpoints

1️. /query - Process Natural Language Query

Method: POST

Request Body:
{ "query": "Total sales amount?" }

Response:
{
    "query": "SELECT SUM(amount) as total_sales FROM sales;",
    "result": [ { "total_sales": 3500 } ]
}


2./explain - Get SQL Translation

Method: POST

Request Body:
{ "query": "How many sales?" }

Response:
{
    "natural_query": "How many sales?",
    "sql_query": "SELECT COUNT(*) as sales_count FROM sales;"
}


3./validate - Check Query Feasibility

Method: POST

Request Body:
{ "query": "Sales by region?" }

Response:
{
    "valid": true,
    "sql_query": "SELECT region, SUM(amount) as total FROM sales GROUP BY region;"
}

 Sample Queries

"Total sales amount?"

"How many orders?"

"Sales by region?"

 Future Enhancements

Support more complex queries

Integrate a real database backend

License

MIT License. Feel free to modify and extend.

Developed with using Flask & SQLite.

Author 
Tejashri Jadhav


