"""
Finance Module - Core classes for Personal Finance Tracker
Demonstrating OOP principles: Classes, Objects, Inheritance
"""

from datetime import datetime
import json
import os
import csv

class Transaction:
    """
    Base class representing a financial transaction
    Demonstrates encapsulation and basic OOP principles
    """
    
    def __init__(self, amount, description, category, transaction_type, timestamp=None):
        """
        Initialize a transaction with validation
        
        Args:
            amount (float): Transaction amount (positive)
            description (str): Transaction description
            category (str): Transaction category
            transaction_type (str): 'income' or 'expense'
            timestamp (datetime): Optional timestamp for loading from storage
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
        self._timestamp = timestamp if timestamp else datetime.now()
    
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
            'timestamp': self._timestamp.isoformat()  # Convert to ISO format string
        }
    
    def to_csv_row(self):
        """Convert transaction to CSV row format"""
        return [
            self._timestamp.isoformat(),
            self._type,
            self._amount,
            self._category,
            self._description
        ]


class RecurringTransaction(Transaction):
    """
    Inherited class for recurring transactions
    Demonstrates inheritance and polymorphism
    """
    
    def __init__(self, amount, description, category, transaction_type, frequency, timestamp=None):
        """
        Initialize recurring transaction
        
        Args:
            frequency (str): 'daily', 'weekly', 'monthly'
            timestamp (datetime): Optional timestamp for loading from storage
        """
        # Call parent class constructor
        super().__init__(amount, description, category, transaction_type, timestamp)
        
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
            next_month = self._timestamp.month + 1
            next_year = self._timestamp.year
            if next_month > 12:
                next_month = 1
                next_year += 1
            return self._timestamp.replace(year=next_year, month=next_month)
    
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
    
    def to_csv_row(self):
        """Override CSV method to include frequency"""
        row = super().to_csv_row()
        row.append(self._frequency)
        return row


class FinanceManager:
    """
    Manages financial transactions and operations
    Demonstrates composition and class relationships
    """
    
    def __init__(self, data_file="transactions.csv"):
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
        """Load transactions from CSV file"""
        if os.path.exists(self._data_file):
            try:
                with open(self._data_file, 'r', newline='') as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)  # Skip header row
                    
                    for row in reader:
                        # Recreate transaction objects from CSV data
                        timestamp = datetime.fromisoformat(row[0])
                        transaction_type = row[1]
                        amount = float(row[2])
                        category = row[3]
                        description = row[4]
                        
                        # Check if it's a recurring transaction
                        if len(row) > 5 and row[5]:  # Has frequency field
                            frequency = row[5]
                            transaction = RecurringTransaction(
                                amount, description, category, transaction_type, frequency, timestamp
                            )
                        else:
                            transaction = Transaction(
                                amount, description, category, transaction_type, timestamp
                            )
                        
                        self._transactions.append(transaction)
                
                print(f" Loaded {len(self._transactions)} transactions from CSV file.")
            except Exception as e:
                print(f" Error loading data: {e}")
    
    def save_to_file(self):
        """Save transactions to CSV file"""
        try:
            with open(self._data_file, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write header row
                writer.writerow(['timestamp', 'type', 'amount', 'category', 'description', 'frequency'])
                
                for transaction in self._transactions:
                    writer.writerow(transaction.to_csv_row())
            
            print(f" Saved {len(self._transactions)} transactions to CSV file.")
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