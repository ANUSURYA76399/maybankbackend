from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from PIL import Image as PILImage
import io
import os
import datetime

class CreditCardStatement:
    def __init__(self, db_path):
        self.db_path = db_path
        self.styles = getSampleStyleSheet()
        self.setup_styles()

    def setup_styles(self):
        # Define all required styles
        self.styles.add(ParagraphStyle(
            name='BankName',
            parent=self.styles['Title'],
            fontSize=28,
            spaceAfter=10,
            textColor=colors.HexColor('#FF0000'),  # Red color
            alignment=1  # Center alignment
        ))

        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#000000'),  # Black color
            fontName='Helvetica-Bold'
        ))

    def create_circular_logo(self):
        try:
            # Use absolute path for the logo
            logo_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'assets',
                'maybank_logo.png'
            )
            
            # Open and process image with PIL first
            pil_img = PILImage.open(logo_path)
            
            # Convert to RGB if necessary
            if pil_img.mode != 'RGB':
                pil_img = pil_img.convert('RGB')
            
            # Save to buffer
            img_buffer = BytesIO()
            pil_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Create ReportLab Image
            img = Image(img_buffer, width=1.5*inch, height=1.5*inch)
            img.hAlign = 'CENTER'
            return img
            
        except Exception as e:
            print(f"Warning: Could not create logo: {str(e)}")
            # Continue without logo
            return None

    def generate_statement_pdf(self, customer_id, customer_name, card_number, zip_code, statement_date, currency, output_path):
        # Create statements directory if it doesn't exist
        statements_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'statements')
        if not os.path.exists(statements_dir):
            os.makedirs(statements_dir)

        # Use the provided output_path if it exists, otherwise generate a default path
        if output_path:
            pdf_path = output_path
        else:
            # Generate default PDF filename
            filename = f"statement_{customer_id}_{statement_date.replace('-', '')}.pdf"
            pdf_path = os.path.join(statements_dir, filename)
        
        # Create the PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        
        story = []

        # Add logo if available
        logo = self.create_circular_logo()
        if logo:
            story.append(logo)
            story.append(Spacer(1, 10))

        # Bank Name Header
        story.append(Paragraph("Maybank Malaysia", self.styles['BankName']))
        story.append(Spacer(1, 10))
        
        # Credit Card Statement Header
        story.append(Paragraph("Credit Card Statement", self.styles['CustomTitle']))
        
        # Customer Information
        customer_info = [
            ["Customer Name:", customer_name],
            ["Customer ID:", customer_id],
            ["Card Number:", "XXXX-XXXX-XXXX-" + card_number[-4:]],
            ["ZIP Code:", zip_code],
            ["Statement Date:", statement_date],
            ["Currency:", currency]
        ]
        
        info_table = Table(customer_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))

        # Account Summary
        story.append(Paragraph("Account Summary", self.styles['SectionHeader']))
        summary_data = [
            ["Previous Balance:", f"{currency} 2,500.00"],
            ["Payments and Credits:", f"{currency} -1,500.00"],
            ["Purchases and Debits:", f"{currency} 3,245.50"],
            ["Fees Charged:", f"{currency} 25.00"],
            ["Interest Charged:", f"{currency} 45.00"],
            ["New Balance:", f"{currency} 4,315.50"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))

        # Transactions
        story.append(Paragraph("Transaction Details", self.styles['SectionHeader']))
        transactions = [
            ["Date", "Description", "Amount", "Type"],
            ["2024-01-01", "Grocery Store", f"{currency} 156.75", "Purchase"],
            ["2024-01-03", "Restaurant Payment", f"{currency} 89.90", "Purchase"],
            ["2024-01-05", "Online Shopping", f"{currency} 299.99", "Purchase"],
            ["2024-01-07", "Utility Bill", f"{currency} 145.50", "Bill Payment"],
            ["2024-01-10", "Previous Balance Payment", f"{currency} 500.00", "Payment"],
            ["2024-01-15", "Electronics Store", f"{currency} 899.99", "Purchase"],
            ["2024-01-18", "Travel Booking", f"{currency} 1250.00", "Purchase"],
            ["2024-01-20", "Insurance Premium", f"{currency} 175.00", "Bill Payment"],
            ["2024-01-22", "Mobile Phone Bill", f"{currency} 85.00", "Bill Payment"],
            ["2024-01-25", "Fuel Purchase", f"{currency} 75.50", "Purchase"],
            ["2024-01-27", "Department Store", f"{currency} 445.75", "Purchase"],
            ["2024-01-28", "Online Subscription", f"{currency} 15.99", "Recurring"],
            ["2024-01-29", "Healthcare", f"{currency} 200.00", "Purchase"],
            ["2024-01-30", "Entertainment", f"{currency} 65.00", "Purchase"],
            ["2024-01-31", "Internet Bill", f"{currency} 89.99", "Bill Payment"]
        ]
        
        trans_table = Table(transactions, colWidths=[1.5*inch, 3*inch, 1.5*inch, 1.5*inch])
        trans_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        story.append(trans_table)
        story.append(Spacer(1, 20))

        # Rewards Summary
        story.append(Paragraph("Rewards Summary", self.styles['SectionHeader']))
        rewards_data = [
            ["Points Earned This Month:", "500 Points"],
            ["Total Points Balance:", "2,500 Points"],
            ["Points Expiring Soon:", "100 Points (Expires in 30 days)"],
            ["Cashback Earned:", f"{currency} 25.00"],
            ["Special Offers:", "10% off at Partner Merchants"]
        ]
        
        rewards_table = Table(rewards_data, colWidths=[3*inch, 3*inch])
        rewards_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        story.append(rewards_table)
        story.append(Spacer(1, 20))

        # Important Notice
        story.append(Paragraph("Important Notice", self.styles['SectionHeader']))
        
        notice_style = ParagraphStyle(
            'Notice',
            parent=self.styles['Normal'],
            fontSize=8,
            leading=10,
            spaceBefore=6,
            spaceAfter=6,
            textColor=colors.black
        )
        
        notice_text = """Please examine this statement immediately. If no error is reported within 14 days, this statement will be considered correct. Late payment charges will be imposed if payment is not received by the due date. Please inform us of any change in your contact details to ensure you receive important updates. For lost/stolen cards, please contact our 24-hour customer service at 1-300-88-6688 immediately. For any inquiries, please visit www.maybank.com.my or contact our customer service."""
        
        story.append(Paragraph(notice_text, notice_style))

        # Build the PDF
        doc.build(story)