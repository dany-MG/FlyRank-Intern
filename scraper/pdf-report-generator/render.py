import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from src.database.report import get_report_data

def generate_pdf_report():
    data = get_report_data()

    # Create the HTML content for the PDF
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; margin-bottom: 40px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            
            thead {{ display: table-header-group; background-color: #f4f4f4; }}
            tr {{ break-inside: avoid; }} 
        </style>
    </head>
    <body>
        <h1>Inventory Report: The Bookstore</h1>
        <p><strong>Generated on:</strong> {datetime.now().strftime("%Y-%m-%d")}</p>
        
        <p><strong>Total of books:</strong> {data['total_books']}</p>
        <p><strong>Average price:</strong> £{data['average_price']}</p>
        
        <h2>Top 5 Most Expensive Books</h2>
        <table>
            <thead><tr><th>Title</th><th>Price</th></tr></thead>
            <tbody>
                {"".join(f"<tr><td>{b['title']}</td><td>£{b['price_gbp']}</td></tr>" for b in data['top_5_expensive'])}
            </tbody>
        </table>
        
        <h2>Catalogue</h2>
        <table>
            <thead><tr><th>Title</th><th>Price</th></tr></thead>
            <tbody>
                {"".join(f"<tr><td>{b['title']}</td><td>£{b['price_gbp']}</td></tr>" for b in data['all_books'])}
            </tbody>
        </table>
    </body>
    </html>
    """

    os.makedirs("reports", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content)
        page.pdf(path="reports/inventory_report.pdf", format="A4", print_background=True)
        browser.close()
    
    print("PDF report generated successfully at 'reports/inventory_report.pdf'.")

if __name__ == "__main__":
    generate_pdf_report()

