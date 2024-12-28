# Expense Tracker Application

## Overview
The Expense Tracker Application is a powerful tool designed to help users efficiently manage their expenses. With a range of intuitive features, this application allows users to track, categorize, analyze, and export their financial data effortlessly. The app aims to simplify expense management while providing a sleek and user-friendly interface.

## Features

### 1. Add Expenses
Users can easily record their daily expenses by providing details such as the amount, category, and date. This ensures accurate tracking of financial activities.

### 2. View Expenses
The application allows users to view all recorded expenses in a tabular or format.

### 3. Expense Categories
Expenses can be categorized (e.g., Food, Transport, Entertainment), making it easier to analyze spending patterns.

### 4. Edit Expense
Users can modify existing expense records in case of errors or updates. This ensures data accuracy.

### 5. Delete Expense
Unwanted or duplicate expense entries can be removed seamlessly.

### 6. Expense Graphs
Visualize your financial data with insightful graphs. These graphs help users identify spending trends and make informed decisions.

### 7. Recurring Expenses (**Coming Soon**)
The app will support recurring expenses, such as subscriptions or monthly bills. These will automatically be added to the user’s expense list, making tracking even more convenient.

### 8. Export Expense
Users can export their expense data in formats for offline storage, reporting, or sharing purposes.

### 9. Dark Mode (Optional)
Switch to Dark Mode for a visually soothing experience, especially useful in low-light environments.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/PS218909/expense-tracker.git
   ```
2. Navigate to the project directory:
   ```bash
   cd expense-tracker
   ```
3. Install dependencies (if applicable):
   ```bash
   pip install -r requirements.txt
   ```
4. Setting up database:
    ```bash
    flask shell
    ```
    ```bash
    from app import db
    db.create_all()
    ```
5. Run the application:
   ```bash
   python -m app
   ```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements or new features.