from datetime import datetime
import easyocr
from cv2 import cvtColor, COLOR_BGR2GRAY
import re
import numpy as np
import supervision as sv

def duration(start_timestamp, end_timestamp):
    """
    Calculate the number of seconds between two timestamps.

    Parameters:
    - start_timestamp: A string representing the start time in "HH:MM:SS" format.
    - end_timestamp: A string representing the end time in "HH:MM:SS" format.

    Returns:
    - The number of seconds between the start and end timestamps as an integer.
    """
    # Convert the start and end timestamps to datetime objects
    start = datetime.strptime(clean_timestamp(start_timestamp), "%H:%M:%S")
    end = datetime.strptime(clean_timestamp(end_timestamp), "%H:%M:%S")

    # Calculate the difference between the two datetime objects
    time_delta = end - start

    # Return the total number of seconds in the time delta
    return int(time_delta.total_seconds())


def format_time(seconds):
    """
    Convert a number of seconds to a string in "HH:MM:SS" format.

    Parameters:
    - seconds: An integer representing the number of seconds to convert.

    Returns:
    - A string representing the number of seconds in "HH:MM:SS" format.
    """
    # Calculate the number of hours, minutes, and seconds
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    # Return the time as a string in "HH:MM:SS" format
    return f"{minutes:02}:{seconds:02}"

# Draw timestamp for time calculations


def draw_timestamp(frame: np.ndarray, x: int, y: int, width: int, height: int, reader) -> str:
    # Extract the Region of Interest (ROI) for OCR
    timestamp_roi = frame[y:y + height, x:x + width]
    
    # Preprocess the ROI as needed (e.g., convert to grayscale)
    timestamp_roi_preprocessed = cvtColor(timestamp_roi, COLOR_BGR2GRAY)
    
    # OCR the preprocessed ROI to extract text
    timestamp_text = reader.readtext(timestamp_roi_preprocessed)
    print("Timestamp text:", timestamp_text)
    
    # Process the OCR result as needed
    # Assuming the `reader.readtext` returns a list of tuples (bounding box, text, confidence)
    if timestamp_text:
        # Extract and join the text from the OCR result
        extracted_text = " ".join([result[1] for result in timestamp_text])
        return extracted_text.strip()
    return ""


import re

def clean_timestamp(timestamp):
    # Extract date and time parts
    date_time_parts = timestamp.split(' ')
    
    if len(date_time_parts) == 2:
        date_part, time_part = date_time_parts
        # Replace incorrect separators in time part
        corrected_time_part = time_part.replace('.', ':')
        
        # Extract digits for more robust formatting (optional)
        numbers = re.findall(r'\d+', corrected_time_part)
        if len(numbers) >= 3:
            hours, minutes, seconds = numbers[-3:]
            corrected_time_part = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        
        return f"{date_part} {corrected_time_part}"
    else:
        # Fallback or error handling if the timestamp format is unexpected
        return "Invalid timestamp format"

