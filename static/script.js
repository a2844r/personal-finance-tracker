
const form = document.getElementById("transaction-form");
const transactionList = document.getElementById("transaction-list");
const categoryFilter = document.getElementById("category-filter");
const summaryCards = document.querySelectorAll(".summary .card h2");

let transactions = [];

function formatMoney(amount) {
    return new Intl.NumberFormat("en-GB", {
        style: "currency",
        currency: "GBP"
    }).format(amount);
}

function updateSummary() {
    const income = transactions
        .filter(t => t.type === "income")
        .reduce((total, t) => total + Number(t.amount), 0);

    const expenses = transactions
        .filter(t => t.type === "expense")
        .reduce((total, t) => total + Number(t.amount), 0);

    summaryCards[0].textContent = formatMoney(income);
    summaryCards[1].textContent = formatMoney(expenses);
    summaryCards[2].textContent = formatMoney(income - expenses);
}


    

function renderTransactions() {
    transactionList.replaceChildren();

    const selectedCategory = categoryFilter.value;

    const filteredTransactions = transactions.filter(transaction => {
        return selectedCategory === "all" ||
            transaction.category === selectedCategory;
    });

    if (filteredTransactions.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 6;
        cell.textContent = transactions.length === 0
            ? "No transactions yet. Add your first one above!"
            : "No transactions found in this category.";

        row.appendChild(cell);
        transactionList.appendChild(row);
        return;
    }

    filteredTransactions.forEach(transaction => {
        const row = document.createElement("tr");

        const values = [
            transaction.date,
            transaction.description || "—",
            transaction.category,
            transaction.type === "income" ? "Income" : "Expense",
            `${transaction.type === "income" ? "+" : "−"}${formatMoney(Number(transaction.amount))}`
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        const actionCell = document.createElement("td");
        const deleteButton = document.createElement("button");

        deleteButton.type = "button";
        deleteButton.textContent = "Delete";
        deleteButton.addEventListener("click", () => {
            deleteTransaction(transaction.id);
        });

        actionCell.appendChild(deleteButton);

const editButton = document.createElement("button");
editButton.type = "button";
editButton.textContent = "Edit";
editButton.className = "edit-button";

editButton.addEventListener("click", () => {
    editTransaction(transaction);
});

actionCell.appendChild(editButton);

        row.appendChild(actionCell);
        transactionList.appendChild(row);
    });
}


categoryFilter.addEventListener("change", renderTransactions);
async function loadTransactions() {
    try {
        const response = await fetch("/api/transactions");

        if (!response.ok) {
            throw new Error("Could not load transactions.");
        }

        transactions = await response.json();
        updateSummary();
        renderTransactions();
        updateSpendingChart();
    } catch (error) {
        console.error(error);
        alert("Couldn't load transactions. Please check that Flask is running.");
    }
}

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const transaction = {
        type: document.getElementById("type").value,
        amount: Number(document.getElementById("amount").value),
        category: document.getElementById("category").value,
        date: document.getElementById("date").value,
        description: document.getElementById("description").value.trim()
    };

    if (
        !transaction.type ||
        !transaction.category ||
        !transaction.date ||
        !Number.isFinite(transaction.amount) ||
        transaction.amount <= 0
    ) {
        alert("Please enter valid transaction details.");
        return;
    }

    try {
        const response = await fetch("/api/transactions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(transaction)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not save transaction.");
        }

        form.reset();
        await loadTransactions();
    } catch (error) {
        console.error(error);
        alert(error.message || "Couldn't save the transaction.");
    }
});

async function deleteTransaction(id) {
    if (!confirm("Are you sure you want to delete this transaction?")) {
        return;
    }

    try {
        const response = await fetch(`/api/transactions/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not delete transaction.");
        }

        await loadTransactions();
    } catch (error) {
        console.error(error);
        alert(error.message || "Couldn't delete the transaction.");
    }
}

loadTransactions();


let spendingChart = null;

function updateSpendingChart() {
    const canvas = document.getElementById("spending-chart");

    if (!canvas) return;

    const expensesByCategory = {};

    transactions
        .filter(transaction => transaction.type === "expense")
        .forEach(transaction => {
            const category = transaction.category || "Other";
            expensesByCategory[category] =
                (expensesByCategory[category] || 0) +
                Number(transaction.amount);
        });

    const categories = Object.keys(expensesByCategory);
    const amounts = Object.values(expensesByCategory);

    if (spendingChart) {
        spendingChart.destroy();
    }

    spendingChart = new Chart(canvas, {
        type: "doughnut",
        data: {
            labels: categories.length ? categories : ["No expenses yet"],
            datasets: [{
                data: amounts.length ? amounts : [1],
                backgroundColor: [
                    "#6658d9",
                    "#f08a5d",
                    "#6abf9b",
                    "#f5c451",
                    "#5b9bd5",
                    "#d779a8",
                    "#9b9b9b"
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            if (!categories.length) {
                                return "No expenses yet";
                            }

                            return `${context.label}: £${context.parsed.toFixed(2)}`;
                        }
                    }
                }
            }
        }
    });
}

const budgetForm = document.getElementById("budget-form");
const budgetList = document.getElementById("budget-list");

async function loadBudgets() {
    const response = await fetch("/api/budgets");
    const budgets = await response.json();

    const transactionResponse = await fetch("/api/transactions");
    const allTransactions = await transactionResponse.json();

    const currentMonth = new Date().toISOString().slice(0, 7);

    budgetList.innerHTML = "";

    if (budgets.length === 0) {
        budgetList.innerHTML = "<p>No budgets yet. Add your first monthly budget above!</p>";
        return;
    }

    budgets.forEach(budget => {
        const spent = allTransactions
            .filter(transaction =>
                transaction.type === "expense" &&
                transaction.category === budget.category &&
                transaction.date &&
                transaction.date.startsWith(currentMonth)
            )
            .reduce((total, transaction) => total + Number(transaction.amount), 0);

        const limit = Number(budget.amount);
        const percentage = limit > 0 ? (spent / limit) * 100 : 0;
        const progress = Math.min(percentage, 100);

        const item = document.createElement("div");
        item.className = "budget-item";

        const heading = document.createElement("h3");
        heading.textContent = budget.category;

        const details = document.createElement("p");
        details.textContent =
            `£${spent.toFixed(2)} spent of £${limit.toFixed(2)} (${percentage.toFixed(0)}%)`;

        const bar = document.createElement("div");
        bar.className = "budget-progress";

        const fill = document.createElement("div");
        fill.className = "budget-progress-fill";
        fill.style.width = `${progress}%`;

        if (percentage >= 100) {
            fill.style.backgroundColor = "#dc3545";
        } else if (percentage >= 80) {
            fill.style.backgroundColor = "#f0ad4e";
        }

        bar.appendChild(fill);
        item.append(heading, details, bar);
        budgetList.appendChild(item);
    });
}

budgetForm.addEventListener("submit", async event => {
    event.preventDefault();

    const category = document.getElementById("budget-category").value;
    const amount = document.getElementById("budget-amount").value;

    try {
        const response = await fetch("/api/budgets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                category,
                amount: Number(amount)
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.error || "Could not save budget.");
            return;
        }

        budgetForm.reset();
        await loadBudgets();
        alert("Budget saved successfully!");
    } catch (error) {
        alert("Could not save the budget. Please try again.");
        console.error(error);
    }
});

loadBudgets();

async function editTransaction(transaction) {
    const type = prompt("Transaction type: enter income or expense", transaction.type);
    if (type === null) return;

    const amountInput = prompt("Amount (£):", transaction.amount);
    if (amountInput === null) return;

    const category = prompt("Category:", transaction.category);
    if (category === null) return;

    const date = prompt("Date (YYYY-MM-DD):", transaction.date);
    if (date === null) return;

    const description = prompt("Description:", transaction.description || "");
    if (description === null) return;

    const updatedTransaction = {
        type: type.trim().toLowerCase(),
        amount: Number(amountInput),
        category: category.trim(),
        date: date.trim(),
        description: description.trim()
    };

    if (
        !["income", "expense"].includes(updatedTransaction.type) ||
        !Number.isFinite(updatedTransaction.amount) ||
        updatedTransaction.amount <= 0 ||
        !updatedTransaction.category ||
        !updatedTransaction.date
    ) {
        alert("Please enter valid transaction details.");
        return;
    }

    try {
        const response = await fetch(
            `/api/transactions/${transaction.id}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(updatedTransaction)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not update transaction.");
        }

        alert("Transaction updated successfully!");
        await loadTransactions();
    } catch (error) {
        console.error(error);
        alert(error.message || "Could not update transaction.");
    }
}



