from statement_generator import CreditCardStatement
import os

def clear_screen():
    os.system('cls')

def display_form(fields):
    clear_screen()
    print("\n=== Credit Card Statement Generator ===\n")
    for field, value in fields.items():
        display_name = field.replace('_', ' ').title()
        print(f"{display_name}: {value if value else '_' * 20}")
    print("\n=====================================\n")

def get_validated_input(prompt, validation_type, fields):
    while True:
        display_form(fields)
        value = input(f"Enter {prompt}: ")
        try:
            if validation_type == "customer_id":
                if len(value) == 8 and value[:2].isalpha() and value[2:].isdigit():
                    return value.upper()
            elif validation_type == "card_number":
                if len(value) == 16 and value.isdigit():
                    return value
            elif validation_type == "zip_code":
                if (len(value) == 5 or len(value) == 10) and value.replace("-", "").isdigit():
                    return value
            elif validation_type == "none":
                return value
            print(f"\nInvalid {validation_type}. Press Enter to try again.")
            input()
        except ValueError:
            print(f"\nInvalid {validation_type}. Press Enter to try again.")
            input()

def main():
    fields = {
        'customer_id': '',
        'customer_name': '',
        'card_number': '',
        'zip_code': '',
        'statement_date': '',
        'currency': '',
        'output_path': ''
    }

    # Get user input with validation
    fields['customer_id'] = get_validated_input("Customer ID (2 letters followed by 6 digits)", "customer_id", fields)
    fields['customer_name'] = get_validated_input("Customer Name", "none", fields)
    fields['card_number'] = get_validated_input("Card Number (16 digits)", "card_number", fields)
    fields['zip_code'] = get_validated_input("ZIP Code (5 digits or 5+4 format)", "zip_code", fields)
    fields['statement_date'] = get_validated_input("Statement Date (YYYY-MM-DD)", "none", fields)
    fields['currency'] = get_validated_input("Currency Symbol ($, €, etc.)", "none", fields)
    fields['output_path'] = get_validated_input("Output PDF path", "none", fields)

    # Display final form
    display_form(fields)
    input("\nPress Enter to generate PDF...")

    # Initialize and generate statement
    try:
        statement = CreditCardStatement("credit_card.db")
        statement.generate_statement_pdf(**fields)
        print("\nPDF generated successfully!")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\nError: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()