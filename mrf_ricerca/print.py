# from bs4 import BeautifulSoup
# from weasyprint import HTML

# # Load your HTML content from a file or URL
# with open('page.html', 'r', encoding='utf-8') as file:
#     html_content = file.read()

# # Parse HTML and extract <main> tag
# soup = BeautifulSoup(html_content, 'html.parser')
# main_tag = soup.find(id='contenuto-principale')

# if main_tag:
#     # Wrap the extracted <main> tag in a basic HTML template
#     html_template = f'''
#     <html>
#     <head>
#         <meta charset="utf-8">
#         <style>
#             body {{ font-family: sans-serif; margin: 20px; }}
#         </style>
#     </head>
#     <body>
#         {str(main_tag)}
#     </body>
#     </html>
#     '''
    
#     # Convert to PDF
#     HTML(string=html_template).write_pdf('main_content.pdf')
#     print("PDF saved as 'main_content.pdf'")
# else:
#     print("No <main> tag found in the HTML.")


import pdfkit
from bs4 import BeautifulSoup

# Read your HTML file
with open("page.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Extract the element with id="contenuto-principale"
soup = BeautifulSoup(html_content, "html.parser")
main_div = soup.find(id="contenuto-principale")

if main_div:
    html_template = f'''
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        {str(main_div)}
    </body>
    </html>
    '''

    pdfkit.from_string(html_template, "main_content.pdf")
    print("PDF saved as 'main_content.pdf'")
else:
    print("Element with id='contenuto-principale' not found.")

