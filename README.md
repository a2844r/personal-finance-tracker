
# Personal Finance Tracker

A personal finance web application built with Python and Flask to help users track income and expenses, manage monthly budgets, and understand their spending habits.

## Features

- **Dashboard:** View income, expenses, and remaining balance.
- **Transaction management:** Add, edit, and delete transactions.
- **Spending breakdown:** Visualise expenses by category using Chart.js.
- **Monthly budgets:** Set category-based budgets and monitor spending progress.
- **Category filtering:** Filter transactions by category.
- **Data persistence:** Store transactions and budgets in SQLite.
- **Input validation:** Reject invalid transaction types and non-positive amounts.
- **Automated testing:** Test application routes, transaction operations, and input validation.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Visualisation:** Chart.js
- **Testing:** Python `unittest`, Flask test client

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd personal-finance-tracker
```

Replace `YOUR_REPOSITORY_URL` with your GitHub repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install Flask
```

### 4. Run the application

```bash
python3 app.py
```

Open http://127.0.0.1:5000 in your browser.

## Running Tests

Run the automated test suite with:

```bash
python3 -m unittest test_app -v
```

The test suite currently contains eight tests covering application routes, transaction creation, updating and deletion, and invalid input handling.

Tests use a temporary database to keep test data separate from the main finance database.

## Project Structure

```text
personal-finance-tracker/
├── app.py
├── test_app.py
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Learning Outcomes

This project demonstrates practical experience with:

- Building web applications using Flask.
- Designing database-backed CRUD operations.
- Using SQLite and parameterised SQL queries.
- Validating user input.
- Writing automated tests.
- Creating responsive interfaces with JavaScript and CSS.

## Future Improvements

- Add user authentication and individual accounts.
- Introduce recurring transactions.
- Add CSV export for financial records.
- Improve transaction editing with a dedicated form.
- Expand test coverage for budget operations and additional invalid inputs.
