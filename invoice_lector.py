import PyPDF2
import re
import pandas as pd

# Open and read PDF
pdf_file = open('invoices.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Creation of the columns I want to work with and an empty list to fill in the extracted information
cols = ['page',
'company_name',
'doc_type',
'number_invoice',
'emission_date',
'product_code',
'product_name',
'amount',
'measure',
'unit_price',
'desc%',
'total_price']

invoice_list_agg = []

# Reading each page
for invoice in range(0, len(pdf_reader.pages)):

    # Extracting the text and transforming it into an array
    page = pdf_reader.pages[invoice]
    text_content = page.extract_text()
    array = text_content.splitlines()

    # Create a list for each invoices to fill the goods
    invoice_list = []

    # Determine the range in which the goods are located
    xo_range = array.index("specific text")
    xf_range = next((i for i, x in enumerate(array) if "other specific text" in x), len(array))

    # Create a loop to collect goods in each row
    for item in range(xo_range + 1, xf_range, 1):

        item_line = array[item]

        # Create a pattern to find the specific string I want to take and fill it in the list 'values'
        pattern_item = r'^(.+?)$'
        match_item = re.match(pattern_item, item_line)
        if match_item:
            values = [match_item.group(1),
            match_item.group(2),
            match_item.group(3),
            match_item.group(4),
            match_item.group(5),
            match_item.group(6),
            match_item.group(7)]

        else:
            continue
        
        # Fill the list with items
        invoice_list = invoice_list + [values]

    # Extract 'page'
    pag = invoice + 1

    # Extract 'company_name'
    company_name = array[0]

    # Extract 'doc_type'
    doctype = array[3]

    # Extract 'number_invoice'
    index_folio = next((i for i, x in enumerate(array) if "Nº " in x), None)
    folio_line = array[index_folio]
    pattern_folio = r"(\d+)$"
    match_folio = re.search(pattern_folio, folio_line).group()

    # Extract 'emission_date'
    index_date = next((i for i, x in enumerate(array) if "some text" in x), None)
    date_line = array[index_date]
    pattern_date = r"(\d{2}.\d{2}.\d{4})"
    match_date = re.search(pattern_date, date_line).group()

    # Completing the list of an invoice
    invoice_list = [[pag] + [company_name] + [doctype] + [match_folio] + [match_date] + sublist for sublist in invoice_list]

    # Fill in the aggregated list with new invoices
    invoice_list_agg = invoice_list_agg + invoice_list

# When the 'invoice_list_agg' is complete, convert to a data frame    
df_invoices_agg = pd.DataFrame(invoice_list_agg, columns = cols)

# Finally, download the data frame in a CSV or other document.
df_invoices_agg.to_csv('extracted_invoices.csv')

# THE END!