import random  # Placeholder for actual scanning logic
import os
from dotenv import load_dotenv
from google.cloud import vision

# def scan_image(image_path):
#     """
#     Simulate scanning an image for an expiration date.
#     Replace this with actual image scanning logic.
#     """

#     # Example of scanned data (replace with your OCR or scanning logic)
#     expiration_date = f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
#     return expiration_date

import re

# Input list of strings
def scan_image(image_path):
    # Define scoring criteria
    MONTHS = {"JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"}
    YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")  # Matches years from 1900 to 2099
    DAY_PATTERN = re.compile(r"\b([0-2][0-9]|3[01])\b")  # Matches days 01-31
    TIME_PATTERN = re.compile(r"\b([01]\d|2[0-3]):?([0-5]\d)\b")  # Matches 24-hour time (HH:MM)

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

        print("Detected text:")
    else:
        print("No text detected.")


    # scored_lines = [(line, score_line(line)) for line in lines]
    # best_line = max(scored_lines, key=lambda x: x[1])

    print(f"Most date-like line: '{best_line[0]}' with score: {best_line[1]}")
    return best_line[0]
