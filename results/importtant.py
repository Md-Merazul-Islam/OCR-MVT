import pdfplumber
import re
import pandas as pd


def parse_pdf(pdf_path):
    results = []

    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            # Split the text by lines (rows of data)
            lines = text.split("\n")

            # Iterate through each line and process it
            for line in lines:
                columns = line.split()  # Split line by spaces to get individual columns

                # Check if the line has at least 8 elements (4 roll number, GPA pairs)
                if len(columns) >= 8:
                    # Iterate in pairs (roll number and GPA)
                    for i in range(0, len(columns), 2):
                        if i + 1 < len(columns):  # Ensure there's a GPA value to access
                            roll_number = columns[i]
                            # Remove parentheses around GPA
                            gpa = columns[i+1].strip("()")

                            # Check if it's a passed case (contains GPA)
                            try:
                                gpa_value = float(gpa)
                                results.append({
                                    "page_number": page_number,
                                    "roll_number": roll_number,
                                    "gpa": gpa_value,
                                    "failed_subjects": None
                                })
                            except ValueError:
                                # Handle failed subjects case (contains subjects in braces)
                                # Remove braces around failed subjects
                                failed_subjects = gpa.strip("{}")
                                results.append({
                                    "page_number": page_number,
                                    "roll_number": roll_number,
                                    "gpa": None,
                                    "failed_subjects": failed_subjects
                                })

    # Return the results as a list of dictionaries
    return results


def save_to_csv(results, output_file="parsed_results.csv"):
    # Convert the results to a pandas DataFrame
    df = pd.DataFrame(results)

    # Save to CSV
    df.to_csv(output_file, index=False)

    print(f"Data has been saved to {output_file}")


if __name__ == "__main__":
    pdf_path = "test.pdf"  # Replace with your actual PDF path
    results = parse_pdf(pdf_path)
    save_to_csv(results)
