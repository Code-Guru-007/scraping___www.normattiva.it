import subprocess
import os

def convert_doc_to_pdf(input_path):
    try:
        print(input_path)
        # Ensure LibreOffice is installed and set the output directory
        output_dir = os.path.dirname(input_path)

        # Run LibreOffice in headless mode to convert the file
        subprocess.run(
            ['soffice', '--headless', '--convert-to', 'pdf', input_path, '--outdir', output_dir],
            check=True
        )

        # print(f"Conversion successful: {os.path.splitext(input_path)[0]}.pdf")
    except Exception as e:
        print(f"Error during conversion: {e}")

# Example usage
convert_doc_to_pdf(os.path.join(os.getcwd(), "test.doc"))
