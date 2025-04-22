import os
from statement_generator import CreditCardStatement

# Define the database path
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')

# Define customer details
customer_id = "AS567898"
customer_name = "John Doe"
card_number = "4532123456789012"
zip_code = "50000"
statement_date = "20240421"
currency = "RM"

# Generate statement
statement_generator = CreditCardStatement(db_path)
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'statements', f"statement_{customer_id}_{statement_date}.pdf")
statement_generator.generate_statement_pdf(
    customer_id=customer_id,
    customer_name=customer_name,
    card_number=card_number,
    zip_code=zip_code,
    statement_date=statement_date,
    currency=currency,
    output_path=output_path
)