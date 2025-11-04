"""
Personal Finance Tracker - Main Application
A comprehensive personal finance management system with OOP principles
"""

import sys
import os
from finance import Transaction, FinanceManager, Budget

def display_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("      PERSONAL FINANCE TRACKER")
    print("="*50)
    print("1. Add Income Transaction")
    print("2. Add Expense Transaction")
    print("3. View All Transactions")
    print("4. View Financial Summary")
    print("5. Set Monthly Budget")
    print("6. View Budget Status")
    print("7. Search Transactions")
    print("8. Exit")
    print("="*50)

def get_user_input(prompt, input_type=str):
    """
    Get validated user input with error handling
    
    Args:
        prompt (str): The prompt to display to user
        input_type (type): Expected data type (str, int, float)
    
    Returns:
        User input in the specified type
    """
    while True:
        try:
            user_input = input(prompt)
            if input_type == str:
                return user_input
            elif input_type == int:
                return int(user_input)
            elif input_type == float:
                return float(user_input)
        except ValueError:
            print(f" Invalid input! Please enter a valid {input_type.__name__}.")

def add_transaction_flow(finance_manager):
    """Handle the transaction addition workflow"""
    print("\n--- Add New Transaction ---")
    
    # Get transaction details with validation
    amount = get_user_input("Enter amount: ", float)
    description = get_user_input("Enter description: ", str)
    category = get_user_input("Enter category: ", str)
    
    # Transaction type selection with loop until valid choice
    while True:
        print("\nTransaction Type:")
        print("1. Income")
        print("2. Expense")
        choice = get_user_input("Select type (1-2): ", int)
        
        if choice == 1:
            transaction_type = "income"
            break
        elif choice == 2:
            transaction_type = "expense"
            break
        else:
            print(" Invalid choice! Please select 1 or 2.")
    
    # Create and add transaction
    transaction = Transaction(amount, description, category, transaction_type)
    finance_manager.add_transaction(transaction)
    print(f" {transaction_type.capitalize()} transaction added successfully!")

def search_transactions_flow(finance_manager):
    """Handle transaction search workflow"""
    print("\n--- Search Transactions ---")
    
    print("Search by:")
    print("1. Category")
    print("2. Description")
    print("3. Amount Range")
    
    choice = get_user_input("Select search option (1-3): ", int)
    
    if choice == 1:
        category = get_user_input("Enter category to search: ", str)
        results = finance_manager.search_by_category(category)
    elif choice == 2:
        description = get_user_input("Enter description to search: ", str)
        results = finance_manager.search_by_description(description)
    elif choice == 3:
        min_amount = get_user_input("Enter minimum amount: ", float)
        max_amount = get_user_input("Enter maximum amount: ", float)
        results = finance_manager.search_by_amount_range(min_amount, max_amount)
    else:
        print(" Invalid choice!")
        return
    
    if results:
        print(f"\n Found {len(results)} transactions:")
        for transaction in results:
            print(f"  - {transaction}")
    else:
        print(" No transactions found matching your criteria.")

def main():
    """Main application entry point with error handling"""
    print(" Initializing Personal Finance Tracker...")
    
    # Initialize finance manager
    finance_manager = FinanceManager()
    budget = Budget(monthly_limit=2000.0)  # Default budget
    
    # Main program loop
    while True:
        try:
            display_menu()
            choice = get_user_input("\nEnter your choice (1-8): ", int)
            
            # Control structure for menu options
            if choice == 1:
                add_transaction_flow(finance_manager)
                
            elif choice == 2:
                add_transaction_flow(finance_manager)
                
            elif choice == 3:
                print("\n--- All Transactions ---")
                finance_manager.display_transactions()
                
            elif choice == 4:
                print("\n--- Financial Summary ---")
                finance_manager.display_summary()
                
            elif choice == 5:
                limit = get_user_input("Enter monthly budget limit: ", float)
                budget.set_monthly_limit(limit)
                print(f" Monthly budget set to ${limit:.2f}")
                
            elif choice == 6:
                print("\n--- Budget Status ---")
                total_expenses = finance_manager.get_total_expenses()
                budget_status = budget.check_budget_status(total_expenses)
                print(budget_status)
                
            elif choice == 7:
                search_transactions_flow(finance_manager)
                
            elif choice == 8:
                print("\n Saving data...")
                finance_manager.save_to_file()
                print(" Thank you for using Personal Finance Tracker!")
                break
                
            else:
                print(" Invalid choice! Please select 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n  Program interrupted by user!")
            finance_manager.save_to_file()
            sys.exit(1)
        except Exception as e:
            print(f" An error occurred: {e}")
            # Debugging information
            print(f"Debug info: Error type - {type(e).__name__}")

# Performance assessment hook
if __name__ == "__main__":
    import time
    start_time = time.time()
    
    main()
    
    end_time = time.time()
    print(f"\n  Program execution time: {end_time - start_time:.2f} seconds")