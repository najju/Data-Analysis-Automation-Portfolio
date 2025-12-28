# Project: Automated Invoice Parser
# Author: Najmuddin Saiyed
# Description: Scrapes data from PDF invoices and saves to a clean Excel report.

import PyPDF2
import pandas as pd
import os

def parse_invoice(pdf_filename):
    """
    Extracts the Total Amount from a single PDF invoice.
    """
    try:
        # Check if file exists
        if not os.path.exists(pdf_filename):
            print(f"❌ Error: '{pdf_filename}' not found.")
            return None

        # Open the PDF
        with open(pdf_filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            page = reader.pages[0]
            text = page.extract_text()

        # Logic to find the amount (Splitting by '$')
        parts = text.split('$')
        if len(parts) > 1:
            amount = parts[1].strip()
            print(f"✅ Extracted: ${amount} from {pdf_filename}")
            return amount
        else:
            print(f"⚠️ No amount found in {pdf_filename}")
            return "0.00"

    except Exception as e:
        print(f"❌ Error reading {pdf_filename}: {e}")
        return None

if __name__ == "__main__":
    
    # 1. Define the file to process (You can loop through a folder later)
    target_file = 'invoice_101.pdf'

    # 2. Run the extraction
    extracted_amount = parse_invoice(target_file)

    if extracted_amount:
        # 3. Save to Excel (The "Money" Step)
        data = {
            'Invoice File': [target_file],
            'Extracted Amount': [extracted_amount],
            'Status': ['Success']
        }

        # Create DataFrame and Save
        df = pd.DataFrame(data)
        output_filename = 'Invoice_Report.csv'
        df.to_csv(output_filename, index=False)
        
        print(f"\n🚀 Success! Report saved to: {output_filename}")
