"""
Finance Module - Core classes for Personal Finance Tracker
Demonstrating OOP principles: Classes, Objects, Inheritance
"""

from datetime import datetime
import json
import os

class Transaction:
    """
    Base class representing a financial transaction
    Demonstrates encapsulation and basic OOP principles
    """
    
    def __init__(self, amount, description, category, transaction_type):
        """
        Initialize a transaction with validation
        
        Args:
            amount (float): Transaction amount (positive)
            description (str): Transaction description
            category (str): Transaction category
            transaction_type (str): 'income' or 'expense'
        """
        # Data validation
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if transaction_type not in ['income', 'expense']:
            raise ValueError("Transaction type must be 'income' or 'expense'")
        
        # Private attributes (encapsulation)
        self._amount = amount
        self._description = description
        self._category = category
        self._type = transaction_type
        self._timestamp = datetime.now()
    
    # Getter methods (property access)
    @property
    def amount(self):
        return self._amount
    
    @property
    def description(self):
        return self._description
    
    @property
    def category(self):
        return self._category
    
    @property
    def type(self):
        return self._type
    
    @property
    def timestamp(self):
        return self._timestamp
    
    def __str__(self):
        """String representation of transaction"""
        sign = "+" if self._type == "income" else "-"
        return (f"[{self._timestamp.strftime('%Y-%m-%d %H:%M')}] "
                f"{sign}${self._amount:.2f} - {self._description} "
                f"({self._category})")
    
    def to_dict(self):
        """Convert transaction to dictionary for serialization"""
        return {
            'amount': self._amount,
            'description': self._description,
            'category': self._category,
            'type': self._type,
            'timestamp': self._timestamp.isoformat()
        }


class RecurringTransaction(Transaction):
    """
    Inherited class for recurring transactions
    Demonstrates inheritance and polymorphism
    """
    
    def __init__(self, amount, description, category, transaction_type, frequency):
        """
        Initialize recurring transaction
        
        Args:
            frequency (str): 'daily', 'weekly', 'monthly'
        """
        # Call parent class constructor
        super().__init__(amount, description, category, transaction_type)
        
        if frequency not in ['daily', 'weekly', 'monthly']:
            raise ValueError("Frequency must be 'daily', 'weekly', or 'monthly'")
        
        self._frequency = frequency
        self._next_occurrence = self._calculate_next_occurrence()
    
    def _calculate_next_occurrence(self):
        """Calculate next occurrence based on frequency"""
        from datetime import timedelta
        
        if self._frequency == 'daily':
            return self._timestamp + timedelta(days=1)
        elif self._frequency == 'weekly':
            return self._timestamp + timedelta(weeks=1)
        elif self._frequency == 'monthly':
            # Simple monthly calculation
            return self._timestamp.replace(month=self._timestamp.month + 1)
    
    @property
    def frequency(self):
        return self._frequency
    
    @property
    def next_occurrence(self):
        return self._next_occurrence
    
    def __str__(self):
        """Polymorphism - override parent's string method"""
        base_str = super().__str__()
        return f"{base_str} [Recurring: {self._frequency}]"


class FinanceManager:
    """
    Manages financial transactions and operations
    Demonstrates composition and class relationships
    """
    
    def __init__(self, data_file="transactions.json"):
        self._transactions = []
        self._data_file = data_file
        self._load_from_file()
    
    def add_transaction(self, transaction):
        """Add a transaction to the manager"""
        if isinstance(transaction, Transaction):
            self._transactions.append(transaction)
            print(f" Transaction added: {transaction}")
        else:
            raise TypeError("Expected Transaction object")
    
    def get_total_income(self):
        """Calculate total income using list comprehension"""
        return sum(t.amount for t in self._transactions if t.type == "income")
    
    def get_total_expenses(self):
        """Calculate total expenses using list comprehension"""
        return sum(t.amount for t in self._transactions if t.type == "expense")
    
    def get_balance(self):
        """Calculate current balance"""
        return self.get_total_income() - self.get_total_expenses()
    
    def display_transactions(self):
        """Display all transactions with looping"""
        if not self._transactions:
            print("No transactions recorded.")
            return
        
        print(f"\nTotal Transactions: {len(self._transactions)}")
        print("-" * 60)
        
        # Loop through transactions with enumeration
        for i, transaction in enumerate(self._transactions, 1):
            print(f"{i}. {transaction}")
    
    def display_summary(self):
        """Display financial summary"""
        total_income = self.get_total_income()
        total_expenses = self.get_total_expenses()
        balance = self.get_balance()
        
        print(f" Total Income: ${total_income:.2f}")
        print(f" Total Expenses: ${total_expenses:.2f}")
        print(f" Current Balance: ${balance:.2f}")
        
        # Performance assessment - transaction count
        print(f" Transaction Count: {len(self._transactions)}")
        
        if total_income > 0:
            savings_rate = ((total_income - total_expenses) / total_income) * 100
            print(f" Savings Rate: {savings_rate:.1f}%")
    
    def search_by_category(self, category):
        """Search transactions by category"""
        return [t for t in self._transactions if t.category.lower() == category.lower()]
    
    def search_by_description(self, description):
        """Search transactions by description"""
        return [t for t in self._transactions if description.lower() in t.description.lower()]
    
    def search_by_amount_range(self, min_amount, max_amount):
        """Search transactions by amount range"""
        return [t for t in self._transactions if min_amount <= t.amount <= max_amount]
    
    def _load_from_file(self):
        """Load transactions from JSON file"""
        if os.path.exists(self._data_file):
            try:
                with open(self._data_file, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        # Recreate transaction objects from dictionary
                        transaction = Transaction(
                            item['amount'],
                            item['description'],
                            item['category'],
                            item['type']
                        )
                        self._transactions.append(transaction)
                print(f" Loaded {len(self._transactions)} transactions from file.")
            except Exception as e:
                print(f" Error loading data: {e}")
    
    def save_to_file(self):
        """Save transactions to JSON file"""
        try:
            data = [t.to_dict() for t in self._transactions]
            with open(self._data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f" Saved {len(self._transactions)} transactions to file.")
        except Exception as e:
            print(f" Error saving data: {e}")


class Budget:
    """
    Budget management class
    Demonstrates additional OOP concepts
    """
    
    def __init__(self, monthly_limit=0.0):
        self._monthly_limit = monthly_limit
        self._categories = {}
    
    def set_monthly_limit(self, limit):
        """Set monthly budget limit"""
        if limit < 0:
            raise ValueError("Budget limit cannot be negative")
        self._monthly_limit = limit
    
    def set_category_limit(self, category, limit):
        """Set budget limit for specific category"""
        self._categories[category] = limit
    
    def check_budget_status(self, current_expenses):
        """Check if expenses are within budget"""
        if self._monthly_limit == 0:
            return "  Monthly budget not set"
        
        percentage = (current_expenses / self._monthly_limit) * 100
        
        if percentage <= 70:
            status = " Within budget"
        elif percentage <= 90:
            status = " Approaching limit"
        else:
            status = " Over budget"
        
        return (f"{status} - ${current_expenses:.2f} / ${self._monthly_limit:.2f} "
                f"({percentage:.1f}%)")