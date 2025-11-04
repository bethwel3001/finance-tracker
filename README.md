# Personal Finance Tracker

A comprehensive personal finance management application built with Python that demonstrates software engineering best practices including OOP, testing, and documentation.

## Features

- **Transaction Management**: Add income and expense transactions
- **Financial Summary**: View balances, totals, and savings rates
- **Budget Tracking**: Set and monitor monthly budgets
- **Search Functionality**: Find transactions by various criteria
- **Data Persistence**: Automatic saving and loading of transactions
- **Recurring Transactions**: Support for regular payments (inheritance demo)


## OOP Principles Demonstrated 

1. **Encapsulation**: Private attributes with getter methods
2. **Inheritance**: `RecurringTransaction` extends `Transaction`
3. **Polymorphism**: Overridden methods in child classes
4. **Composition**: `FinanceManager` contains `Transaction` objects

## Control Structures Used

- **Conditional Statements**: if/elif/else for menu navigation
- **Loops**: while loops for main program, for loops for transactions
- **Exception Handling**: try/except blocks for robust error handling

## Installation & Usage 

1. **Clone/Download** the project files
2. **Navigate** to the project directory:
```bash
cd finance_tracker
```
3. **Run the program**
```bash
python3 main.py
```   
4. Run tests (optional)
```bash
python3 test_finance.py
```

## The application includes:
- Execution time measurement
- Transaction processing performance tests
- Memory-efficient data structures
- Optimized search algorithms
# See `DESIGN.md` for detailed design documentation and `flowchart.png` for visual program flow.

