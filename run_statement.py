from statement_generator import CreditCardStatement

def main():
    # Initialize the statement generator with a database path
    db_path = "credit_card.db"
    statement = CreditCardStatement(db_path)

    # Example customer data
    customer_id = "AB123456"  # Format: 2 letters followed by 6 digits
    customer_name = "John Doe"
    card_number = "4532123456789012"  # 16 digits
    zip_code = "12345"
    statement_date = "2023-11-15"
    currency = "$"
    output_path = "credit_card_statement.pdf"

    try:
        statement.generate_statement_pdf(
            customer_id=customer_id,
            customer_name=customer_name,
            card_number=card_number,
            zip_code=zip_code,
            statement_date=statement_date,
            currency=currency,
            output_path=output_path
        )
        print(f"Statement generated successfully at: {output_path}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()