"""
Test Module for Personal Finance Tracker
Demonstrating unit testing and debugging
"""

import unittest
import os
import tempfile
from finance import Transaction, RecurringTransaction, FinanceManager, Budget

class TestTransaction(unittest.TestCase):
    """Test cases for Transaction class"""
    
    def test_transaction_creation(self):
        """Test basic transaction creation"""
        transaction = Transaction(100.0, "Salary", "Income", "income")
        self.assertEqual(transaction.amount, 100.0)
        self.assertEqual(transaction.description, "Salary")
        self.assertEqual(transaction.type, "income")
    
    def test_invalid_amount(self):
        """Test transaction with invalid amount"""
        with self.assertRaises(ValueError):
            Transaction(-50.0, "Test", "Food", "expense")
    
    def test_invalid_type(self):
        """Test transaction with invalid type"""
        with self.assertRaises(ValueError):
            Transaction(50.0, "Test", "Food", "invalid_type")

class TestRecurringTransaction(unittest.TestCase):
    """Test cases for RecurringTransaction class"""
    
    def test_recurring_transaction(self):
        """Test recurring transaction creation"""
        recurring = RecurringTransaction(50.0, "Netflix", "Entertainment", "expense", "monthly")
        self.assertEqual(recurring.frequency, "monthly")
        self.assertIsNotNone(recurring.next_occurrence)

class TestFinanceManager(unittest.TestCase):
    """Test cases for FinanceManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_file = tempfile.mktemp()
        self.manager = FinanceManager(self.temp_file)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_add_transaction(self):
        """Test adding transactions"""
        transaction = Transaction(100.0, "Test Income", "Salary", "income")
        self.manager.add_transaction(transaction)
        self.assertEqual(len(self.manager._transactions), 1)
    
    def test_balance_calculation(self):
        """Test balance calculation"""
        income = Transaction(1000.0, "Salary", "Income", "income")
        expense = Transaction(200.0, "Food", "Groceries", "expense")
        
        self.manager.add_transaction(income)
        self.manager.add_transaction(expense)
        
        self.assertEqual(self.manager.get_balance(), 800.0)
        self.assertEqual(self.manager.get_total_income(), 1000.0)
        self.assertEqual(self.manager.get_total_expenses(), 200.0)

class TestBudget(unittest.TestCase):
    """Test cases for Budget class"""
    
    def test_budget_creation(self):
        """Test budget creation and limits"""
        budget = Budget(1000.0)
        self.assertEqual(budget._monthly_limit, 1000.0)
    
    def test_budget_status(self):
        """Test budget status calculation"""
        budget = Budget(1000.0)
        status = budget.check_budget_status(500.0)
        self.assertIn("Within budget", status)

# Performance tests
class TestPerformance(unittest.TestCase):
    """Performance testing for finance operations"""
    
    def test_transaction_performance(self):
        """Test performance with multiple transactions - FIXED"""
        import time
        
        manager = FinanceManager()
        
        # Add multiple transactions - START FROM 1, NOT 0 (amount must be positive)
        start_time = time.time()
        
        for i in range(1, 101):  # From 1 to 100
            transaction = Transaction(float(i), f"Test {i}", "Category", "income")
            manager.add_transaction(transaction)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Performance assertion - should complete in reasonable time
        self.assertLess(execution_time, 1.0, "Transaction addition too slow")
        print(f"Performance: Added 100 transactions in {execution_time:.4f} seconds")

if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)