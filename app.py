
from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)


DATABASE = Path(__file__).with_name("finance.db")


def get_db_connection():
    database_path = app.config.get("DATABASE", DATABASE)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection



def initialise_database():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT ''
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL UNIQUE,
                amount REAL NOT NULL CHECK(amount > 0)
            )
        """)



initialise_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    with get_db_connection() as connection:
        rows = connection.execute("""
            SELECT id, type, amount, category, date, description
            FROM transactions
            ORDER BY date DESC, id DESC
        """).fetchall()

    return jsonify([dict(row) for row in rows])


@app.route("/api/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid transaction data."}), 400

    transaction_type = data.get("type")
    category = data.get("category")
    date = data.get("date")
    description = data.get("description", "")

    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "Enter a valid amount."}), 400

    if transaction_type not in ("income", "expense"):
        return jsonify({"error": "Choose income or expense."}), 400

    if not isinstance(category, str) or not category.strip():
        return jsonify({"error": "Choose a category."}), 400

    if not isinstance(date, str) or len(date) != 10:
        return jsonify({"error": "Enter a valid date."}), 400

    if amount <= 0 or amount != amount or amount == float("inf"):
        return jsonify({"error": "Amount must be greater than zero."}), 400

    amount = round(amount, 2)

    if not isinstance(description, str):
        return jsonify({"error": "Invalid description."}), 400

    with get_db_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO transactions
                (type, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            transaction_type,
            amount,
            category.strip(),
            date,
            description.strip()
        ))

        transaction_id = cursor.lastrowid

        row = connection.execute("""
            SELECT id, type, amount, category, date, description
            FROM transactions
            WHERE id = ?
        """, (transaction_id,)).fetchone()

    return jsonify(dict(row)), 201



@app.route("/api/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    with get_db_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Transaction not found."}), 404

    return jsonify({"message": "Transaction deleted successfully."})

@app.route("/api/transactions/<int:transaction_id>", methods=["PUT"])
def edit_transaction(transaction_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid transaction data."}), 400

    transaction_type = data.get("type")
    category = data.get("category")
    date = data.get("date")
    description = data.get("description", "")

    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "Enter a valid amount."}), 400

    if transaction_type not in ("income", "expense"):
        return jsonify({"error": "Choose income or expense."}), 400

    if not isinstance(category, str) or not category.strip():
        return jsonify({"error": "Choose a category."}), 400

    if not isinstance(date, str) or not date.strip():
        return jsonify({"error": "Choose a date."}), 400

    if not isinstance(description, str):
        return jsonify({"error": "Invalid description."}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero."}), 400

    with get_db_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE transactions
            SET type = ?, amount = ?, category = ?, date = ?, description = ?
            WHERE id = ?
            """,
            (
                transaction_type,
                amount,
                category.strip(),
                date,
                description.strip(),
                transaction_id
            )
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Transaction not found."}), 404

    return jsonify({"message": "Transaction updated successfully."})

@app.route("/api/budgets", methods=["GET"])
def get_budgets():
    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM budgets ORDER BY category"
        ).fetchall()

    return jsonify([dict(row) for row in rows])


@app.route("/api/budgets", methods=["POST"])
def save_budget():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid budget data."}), 400

    category = data.get("category")

    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "Enter a valid budget amount."}), 400

    if not isinstance(category, str) or not category.strip():
        return jsonify({"error": "Choose a category."}), 400

    if not category.strip() or amount <= 0:
        return jsonify({"error": "Budget must be greater than zero."}), 400

    with get_db_connection() as connection:
        connection.execute(
            """
            INSERT INTO budgets (category, amount)
            VALUES (?, ?)
            ON CONFLICT(category)
            DO UPDATE SET amount = excluded.amount
            """,
            (category.strip(), amount)
        )

    return jsonify({"message": "Budget saved successfully."}), 201


if __name__ == "__main__":
    app.run(debug=True)
