# Backend Maybank

A professional credit card statement generator application that creates personalized PDF statements for customers.

## Features

- Generate professional credit card statements in PDF format
- Personalized statements including:
  - Customer Name
  - Customer ID
  - Card Number (masked for security)
  - Statement Date
  - ZIP Code
  - Currency Selection (USD, EUR, GBP, JPY, MYR, SGD)

## Statement Generation

The application generates professional PDF statements with the following details:
- Customer identification details prominently displayed
- Secure card information handling
- Downloadable PDF format
- Unique filename format: `statement_[CustomerID]_[Date].pdf`

## Input Validation

The system includes comprehensive validation for:
- Card number verification
- Customer ID format (4-digit number)
- Valid customer name format
- ZIP code validation
- Date format checking
- Currency validation

## Usage

1. Enter the required customer information in the form
2. Click "Generate Statement" to create the PDF
3. Use "Download PDF" to access the generated statement
4. Statements are saved in the `statements` folder with unique identifiers

## Requirements

- Python 3.x
- Tkinter for GUI
- PDF generation capabilities
- SQLite database for data storage