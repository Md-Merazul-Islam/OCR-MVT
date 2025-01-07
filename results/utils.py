# import pdfplumber
# import re

# def parse_pdf(pdf_path):
#     results = []

#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             lines = text.split("\n")

#             for line in lines:
#                 # Handle failed case
#                 if "{" in line:
#                     match = re.match(r"(\d+)\s*\{\s*(.+)\s*\}", line)
#                     # print(match.group)
#                     if match:
#                         roll = match.group(1)
#                         failed_subjects = match.group(2).split(", ")
#                         results.append({
#                             "roll_number": roll.strip(),
#                             "is_passed": False,
#                             "gpa": None,
#                             "failed_subjects": ", ".join(failed_subjects)
#                         })
                
#                 # Handle passed case
#                 elif "(" in line:
#                     match = re.match(r"(\d+)\s*\(\s*([\d.]+)\s*\)", line)
#                     if match:
#                         roll = match.group(1)
#                         gpa = match.group(2)
#                         results.append({
#                             "roll_number": roll.strip(),
#                             "is_passed": True,
#                             "gpa": float(gpa),
#                             "failed_subjects": None
#                         })

#     return results



import pdfplumber
import re

def parse_pdf(pdf_path):
    results = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")

            for line in lines:
                # Handle passed students: Look for roll number followed by GPA in parentheses
                if "(" in line and ")" in line and "{" not in line:
                    match = re.match(r"(\d{6,7})\s*\(\s*([\d.]+)\s*\)", line)
                    if match:
                        roll = match.group(1)
                        gpa = match.group(2)
                        results.append({
                            "roll_number": roll.strip(),
                            "is_passed": True,
                            "gpa": float(gpa),
                            "failed_subjects": None
                        })
                
                # Handle failed students: Look for roll number followed by failed subjects in curly braces
                elif "{" in line and "}" in line:
                    match = re.match(r"(\d{6,7})\s*\{\s*(.*?)\s*\}", line)
                    if match:
                        roll = match.group(1)
                        failed_subjects = match.group(2)
                        results.append({
                            "roll_number": roll.strip(),
                            "is_passed": False,
                            "gpa": None,
                            "failed_subjects": failed_subjects
                        })

    return results
