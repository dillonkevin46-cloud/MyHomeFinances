# FamilyFinance

A Django application for managing household finances, designed for easy deployment on Windows.

## Prerequisites

-   Python 3.10+ installed and added to your PATH.
-   Access to the command prompt.

## Setup Instructions (Windows)

1.  **Extract the project files.**
2.  **Run `install.bat`** (double-click or run from command prompt):
    -   This script will install the required Python packages (`requirements.txt`).
    -   Apply the database migrations (`python manage.py migrate`). This is crucial to create the necessary tables.
    -   Populate initial sample data (`python populate_data.py`).

## Running the Application

1.  **Run `run.bat`**:
    -   This will start the development server at `http://127.0.0.1:8000/`.
    -   It will also attempt to open your default browser to the dashboard.

## Manual Setup (Alternative)

If you prefer running commands manually:

1.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Apply migrations:
    ```bash
    python manage.py migrate
    ```
4.  Populate data:
    ```bash
    python populate_data.py
    ```
5.  Run server:
    ```bash
    python manage.py runserver
    ```

## Features

-   **Dashboard:** Overview of budget, expenses, and remaining funds.
-   **Filters:** View expenses for "Husband", "Wife", or "Joint" accounts individually.
-   **Visuals:** Budget vs Actual and Expense Breakdown charts using Chart.js.
-   **Transactions:** Add and view transactions.
-   **Rollover Logic:** Calculates remaining budget based on limits and previous rollovers.

## Troubleshooting

-   **"no such table: finance_budget"**: This means you haven't run the migrations. Ensure you run `install.bat` or `python manage.py migrate` before starting the server.
