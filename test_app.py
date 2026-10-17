
import os
import tempfile
import unittest

import app as finance_app


class FinanceTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()

        finance_app.app.config["TESTING"] = True
        finance_app.app.config["DATABASE"] = self.temp_db.name

        finance_app.initialise_database()
        self.client = finance_app.app.test_client()

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_homepage_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    
    def test_create_transaction(self):
        response = self.client.post(
            "/api/transactions",
            json={
                "type": "expense",
                "amount": 25.50,
                "category": "Food",
                "date": "2026-10-17",
                "description": "Test lunch"
            }
        )

        self.assertIn(response.status_code, [200, 201])

        transactions_response = self.client.get("/api/transactions")
        transactions = transactions_response.get_json()

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["category"], "Food")

    def test_transactions_endpoint_returns_list(self):
        response = self.client.get("/api/transactions")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    
    def test_rejects_negative_amount(self):
        response = self.client.post(
            "/api/transactions",
            json={
                "type": "expense",
                "amount": -25,
                "category": "Food",
                "date": "2026-10-17",
                "description": "Invalid test"
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    
    def test_rejects_invalid_transaction_type(self):
        response = self.client.post(
            "/api/transactions",
            json={
                "type": "transfer",
                "amount": 25,
                "category": "Food",
                "date": "2026-10-17",
                "description": "Invalid test"
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    
    def test_delete_transaction(self):
        create_response = self.client.post(
            "/api/transactions",
            json={
                "type": "expense",
                "amount": 10,
                "category": "Food",
                "date": "2026-10-17",
                "description": "Delete test"
            }
        )

        self.assertIn(create_response.status_code, [200, 201])

        transactions = self.client.get(
            "/api/transactions"
        ).get_json()

        transaction_id = transactions[0]["id"]

        delete_response = self.client.delete(
            f"/api/transactions/{transaction_id}"
        )

        self.assertEqual(delete_response.status_code, 200)

        remaining = self.client.get(
            "/api/transactions"
        ).get_json()

        self.assertEqual(len(remaining), 0)

    
    def test_update_transaction(self):
        create_response = self.client.post(
            "/api/transactions",
            json={
                "type": "expense",
                "amount": 10,
                "category": "Food",
                "date": "2026-10-17",
                "description": "Original transaction"
            }
        )

        self.assertIn(create_response.status_code, [200, 201])

        transactions = self.client.get(
            "/api/transactions"
        ).get_json()

        transaction_id = transactions[0]["id"]

        update_response = self.client.put(
            f"/api/transactions/{transaction_id}",
            json={
                "type": "expense",
                "amount": 20,
                "category": "Food",
                "date": "2026-10-17",
                "description": "Updated transaction"
            }
        )

        self.assertEqual(update_response.status_code, 200)

        updated_transactions = self.client.get(
            "/api/transactions"
        ).get_json()

        self.assertEqual(updated_transactions[0]["amount"], 20)
        self.assertEqual(
            updated_transactions[0]["description"],
            "Updated transaction"
        )

    def test_budgets_endpoint_returns_list(self):
        response = self.client.get("/api/budgets")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)


if __name__ == "__main__":
    unittest.main()
