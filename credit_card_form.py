import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import datetime
from validation import validate_card_number, validate_zip_code, validate_currency
from statement_generator import CreditCardStatement
import os

class CreditCardForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Credit Card Statement Generator")
        self.root.geometry("500x600")

        # Create form fields
        self.create_form()

    def create_form(self):
        # Card Details Frame
        details_frame = ttk.LabelFrame(self.root, text="Card Details", padding=20)
        details_frame.pack(fill="x", padx=10, pady=5)

        # Card Number
        ttk.Label(details_frame, text="Card Number:").grid(row=0, column=0, sticky="w")
        self.card_number = ttk.Entry(details_frame, width=30)
        self.card_number.grid(row=0, column=1, pady=5)

        # Customer Name
        ttk.Label(details_frame, text="Customer Name:").grid(row=1, column=0, sticky="w")
        self.customer_name = ttk.Entry(details_frame, width=30)
        self.customer_name.grid(row=1, column=1, pady=5)

        # Customer ID
        ttk.Label(details_frame, text="Customer ID:").grid(row=2, column=0, sticky="w")
        self.customer_id = ttk.Entry(details_frame, width=30)
        self.customer_id.grid(row=2, column=1, pady=5)

        # ZIP Code
        ttk.Label(details_frame, text="ZIP Code:").grid(row=3, column=0, sticky="w")
        self.zip_code = ttk.Entry(details_frame, width=30)
        self.zip_code.grid(row=3, column=1, pady=5)

        # Statement Date
        ttk.Label(details_frame, text="Statement Date:").grid(row=4, column=0, sticky="w")
        self.statement_date = ttk.Entry(details_frame, width=30)
        self.statement_date.grid(row=4, column=1, pady=5)
        self.statement_date.insert(0, "YYYY-MM-DD")

        # Currency
        ttk.Label(details_frame, text="Currency:").grid(row=5, column=0, sticky="w")
        self.currency = ttk.Combobox(details_frame, values=['USD', 'EUR', 'GBP', 'JPY', 'MYR', 'SGD', 'INR'], width=27)
        self.currency.grid(row=5, column=1, pady=5)

        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)

        # Generate Button
        generate_btn = ttk.Button(self.root, text="Generate Statement", command=self.generate_statement)
        generate_btn.pack(pady=20)

        # Download Button
        download_btn = ttk.Button(button_frame, text="Download PDF", command=self.open_pdf)
        download_btn.pack(side='left', padx=5)

    def open_pdf(self):
        try:
            output_path = f'statements/statement_{self.customer_id.get()}_{datetime.now().strftime("%Y%m%d")}.pdf'
            if os.path.exists(output_path):
                os.startfile(os.path.abspath(output_path))
            else:
                messagebox.showerror("Error", "Please generate the statement first!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PDF: {str(e)}")

    def validate_inputs(self):
        # Check for empty fields
        if not self.card_number.get().strip():
            messagebox.showerror("Error", "Card number is required")
            return False
        if not self.customer_name.get().strip():
            messagebox.showerror("Error", "Customer name is required")
            return False
        if not self.customer_id.get().strip():
            messagebox.showerror("Error", "Customer ID is required")
            return False
        if not self.zip_code.get().strip():
            messagebox.showerror("Error", "ZIP code is required")
            return False
        if not self.statement_date.get().strip():
            messagebox.showerror("Error", "Statement date is required")
            return False
        if not self.currency.get().strip():
            messagebox.showerror("Error", "Currency is required")
            return False

        # Validate card number
        if not validate_card_number(self.card_number.get()):
            messagebox.showerror("Error", "Invalid card number")
            return False

        # Validate ZIP code
        if not validate_zip_code(self.zip_code.get()):
            messagebox.showerror("Error", "Invalid ZIP code format (must be 5 or 6 digits)")
            return False

        # Validate customer ID format (2 letters followed by 6 digits)
        customer_id = self.customer_id.get().strip()
        if not re.match(r'^[A-Za-z]{2}\d{6}$', customer_id):
            messagebox.showerror("Error", "Customer ID must be 2 letters followed by 6 digits (e.g., AB123456)")
            return False

        # Validate customer name (only letters, spaces, and basic punctuation)
        if not re.match(r'^[A-Za-z\s\'\-\.]{2,50}$', self.customer_name.get()):
            messagebox.showerror("Error", "Invalid customer name (use only letters, spaces, and basic punctuation)")
            return False

        # Validate date
        try:
            datetime.strptime(self.statement_date.get(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return False

        # Validate currency
        if not validate_currency(self.currency.get()):
            messagebox.showerror("Error", "Please select a valid currency")
            return False

        return True

    def generate_statement(self):
        if not self.validate_inputs():
            return

        try:
            # Create directories if they don't exist
            if not os.path.exists('database'):
                os.makedirs('database')
            if not os.path.exists('statements'):
                os.makedirs('statements')

            # Initialize statement generator
            statement_gen = CreditCardStatement('database/credit_card.db')

            # Generate PDF
            output_path = f'statements/statement_{self.customer_id.get()}_{datetime.now().strftime("%Y%m%d")}.pdf'
            
            statement_gen.generate_statement_pdf(
                customer_id=self.customer_id.get(),
                customer_name=self.customer_name.get(),
                card_number=self.card_number.get(),
                zip_code=self.zip_code.get(),
                statement_date=self.statement_date.get(),
                currency=self.currency.get(),
                output_path=output_path
            )

            messagebox.showinfo("Success", f"Statement generated successfully!\nLocation: {os.path.abspath(output_path)}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate statement: {str(e)}")

def main():
    root = tk.Tk()
    app = CreditCardForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()