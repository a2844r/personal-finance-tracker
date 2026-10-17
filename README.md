# Personal Finance Tracker

A personal finance dashboard built with Flask, SQLite, HTML, CSS and JavaScript. The application helps users record transactions, monitor their balance, visualise spending and manage monthly budgets.

## Features

- **Transaction management:** Add, edit and delete income and expense records.
- **Financial summaries:** View total income, expenses and remaining balance.
- **Spending visualisation:** Explore expense categories using a doughnut chart.
- **Monthly budgets:** Set category-specific budgets and track spending against limits.
- **Category filtering:** Filter transactions by category.
- **Data persistence:** Store transaction and budget data in an SQLite database.
- **Input validation:** Validate transaction details before saving them.
- **Automated testing:** Test application routes and transaction functionality using Python's `unittest` framework.

## Technology Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Visualisation:** Chart.js
- **Testing:** Python `unittest`
- **Version control:** Git and GitHub

## Getting Started

### Prerequisites

- Python 3
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/a2844r/personal-finance-tracker.git
   cd personal-finance-tracker
   ```

2. Create and activate a virtual environment:

   **macOS/Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python3 app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.

The SQLite database is initialised by the application when needed.

## Running the Tests

Run the automated test suite with:

```bash
python3 -m unittest test_app -v
```

The tests cover application endpoints and transaction operations.

## Project Structure

```text
personal-finance-tracker/
├── app.py
├── test_app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── script.js
    └── style.css
```

## Future Improvements

- Replace browser prompts with a dedicated transaction-editing modal.
- Add date-range filtering and monthly financial reports.
- Improve automated test coverage for budget validation and error handling.

## Disclaimer

This project is intended for personal learning and demonstration. Use fictional data when showcasing the application publicly.
