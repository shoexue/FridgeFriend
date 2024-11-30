import os
from dotenv import load_dotenv
from google.cloud import vision

import re

# Define scoring criteria
MONTHS = {"JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"}
YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")  # Matches years from 1900 to 2099
DAY_PATTERN = re.compile(r"\b([0-2][0-9]|3[01])\b")  # Matches days 01-31
TIME_PATTERN = re.compile(r"\b([01]\d|2[0-3]):?([0-5]\d)\b")  # Matches 24-hour time (HH:MM)


MONTH_MAP = {
    "JAN": "01", "FEB": "02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06", "JN": "06",
    "JUL": "07", "AUG": "08", "AU": "08","SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12",
    "FE": "02", "OC": "10"  # Handle scanned anomalies
}
def standardize_date(date_str):
    """
    Converts a date-like string into the format YYYY-MM-DD.
    Loops through the string to find valid day, month, and year components.
    """
    # Normalize separators and whitespace
    date_str = date_str.upper().replace("/", " ").replace("-", " ").replace(",", " ").strip()

    print(f"Normalized string: {date_str}")
    
    # Initialize variables
    day, month, year = None, None, None
    
    # Split the string into parts
    parts = date_str.split()

    # Loop through each part and identify if it corresponds to a valid day, month, or year
    for part in parts:
        if part in MONTH_MAP:  # If part is a valid month
            month = MONTH_MAP[part]
        elif re.match(r"\b(19|20)\d{2}\b", part):  # If part is a valid year (e.g., 2024)
            year = part
        elif re.match(r"\b([0-2]?[0-9]|3[01])\b", part):  # If part is a valid day (e.g., 01, 12, 25)
            day = part.zfill(2)  # Ensure two digits for day

    # If all parts are identified correctly, return the standardized date
    if year and month and day:
        return f"{year}-{month}-{day}"

    # If any part is missing, return an error message
    return f"Could not standardize: {date_str}"

# def standardize_date(date_str):
#     """
#     Converts a date-like string into the format YYYY-MM-DD.
#     """
#     # Normalize separators and whitespace
#     date_str = date_str.upper().replace("/", " ").replace("-", " ").replace(",", " ").strip()

#     print(date_str)
#     date_str = re.sub(r"[^\dA-Za-z ]", "", date_str)  # Remove non-alphanumeric characters except spaces
#     print(date_str)
            
#     parts = date_str.split()

#     # If the string has three parts, assume it's in the format DAY MONTH YEAR or similar
#     if len(parts) == 3:
#         day, month, year = None, None, None

#         # Check for month part
#         for part in parts:
#             if part in MONTH_MAP:
#                 month = MONTH_MAP[part]
#             elif re.match(r"\b(19|20)\d{2}\b", part):  # Check for year
#                 year = part
#             elif re.match(r"\b([0-2]?[0-9]|3[01])\b", part):  # Check for day
#                 day = part.zfill(2)  # Ensure two digits for day

#         # If any part is missing, return the original string
#         if not (day and month and year):
#             return f"Could not standardize: {date_str}"

#         return f"{year}-{month}-{day}"

#     # If the string has two parts, infer year or day
#     elif len(parts) == 2:
#         month, year,day = None, None, None

#         for part in parts:
#             if part in MONTH_MAP:
#                 month = MONTH_MAP[part]
#             elif re.match(r"\b(19|20)\d{2}\b", part):  # Check for year
#                 year = part
#             else:  # Assume the remaining part is the day
#                 day = part.zfill(2)

#         if month and year and day:
#             return f"{year}-{month}-{day}"

#     return f"Could not standardize: {date_str}"



def score_line(line):
    score = 0
    
    # Check for a month abbreviation
    if any(month in line.upper() for month in MONTHS):
        score += 1
    
    # Check for a year
    if YEAR_PATTERN.search(line):
        score += 1
    
    # Check for a day
    if DAY_PATTERN.search(line):
        score += 1
    
    # Check for time
    if TIME_PATTERN.search(line):
        score += 1
    
    # Check for common separators in date formats (e.g., space, slash, colon)
    if any(sep in line for sep in [" ", "/", "-", ":"]):
        score += 1
    
    return score

# Input list of strings
def scan_image(image_path):

    # Find the line with the highest score

    load_dotenv()
    service_account_path = os.getenv("SERVICE_PATH")
    
    # Programmatically set the environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path

    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:

    # with open("/Users/jus/Downloads/food.jpeg", "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    # Extract detected text
    texts = response.text_annotations
    if texts:
        lines = texts[0].description.split('\n')
        scored_lines = [(text, score_line(text)) for text in lines]
        best_line = max(scored_lines, key=lambda x: x[1])

        print(f"Most date-like line: '{best_line[0]}' with score: {best_line[1]}")
        std = standardize_date(best_line[0])

        if std.startswith("Could not standardize"):
            print(f"Standardization failed for text: {best_line[0]}")
            return None  # Indicate failure
        print(f"Standardized: {std}")
        return std

    else:
        print("No text detected.")
        return None