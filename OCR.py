import easyocr
import re


def text(image_path):
    # Initialize the reader
    reader = easyocr.Reader(['en'])  # Specify the language(s) you need
    
    # Read the text from the image
    result = reader.readtext(image_path)
    
    # Extract text from the result
    extracted_text = ' '.join([text[1] for text in result])
    
    return extracted_text

def HomeTeam_awayTeam(image_path):
    # Initialize the reader
    reader = easyocr.Reader(['en'])  # Specify the language(s) you need
    
    # Read the text from the image
    result = reader.readtext(image_path)
    
    # Extract text from the result
    extracted_text = ' '.join([text[1] for text in result])
    
    # Use regex to find the pattern (text number-number text)
    match = re.search(r'([a-zA-Z]+)\s\d+-\d+\s([a-zA-Z]+)', extracted_text)
    
    if match:
        first_text = match.group(1)
        second_text = match.group(2)
    else:
        first_text = None
        second_text = None
    
    return first_text, second_text

def Substitution(image_path):
    # Initialize the reader
    reader = easyocr.Reader(['en'])  # Specify the language(s) you need
    
    # Read the text from the image
    result = reader.readtext(image_path)
    
    # Sort the result based on the y-coordinate of the bounding box to determine the lines
    sorted_result = sorted(result, key=lambda x: x[0][0][1])
    
    # Extract text from the sorted result
    lines = [text[1] for text in sorted_result]
    
    # Initialize variables for first and second lines
    first_line = None
    second_line = None
    
    # Assign the first and second lines if they exist
    if len(lines) > 0:
        first_line = lines[0]
    if len(lines) > 1:
        second_line = lines[1]
    
    return first_line, second_line
def SB(image_path):
    # Initialize the reader
    reader = easyocr.Reader(['en'])  # Specify the language(s) you need
    
    # Read the text from the image
    result = reader.readtext(image_path)
    
    # Extract text from the result
    extracted_text = ' '.join([text[1] for text in result])
    
    # Split the text on '-' to get numbers
    parts = extracted_text.split('-')
    
    # Convert parts to integers
    if len(parts) == 2:
        try:
            num1 = int(parts[0].strip())
            num2 = int(parts[1].strip())
            return (num1, num2)
        except ValueError:
            return None  # Return None if conversion fails
    else:
        return None  # Return None if format is not as expected

#Example usage
# image_path = 'EPL3\crop_event.jpg'  # Replace with your image path
# text = text(image_path)
# print(text)

# image_path = 'htat.png'  # Update with the path to your image
# first_text, second_text = HomeTeam_awayTeam(image_path)
# print(f"First text: {first_text}, Second text: {second_text}")

# print(SB('Capture.png'))

# image_path = 'Capture.PNG'  # Update with the path to your image
# first_text, second_text = Substitution(image_path)
# print(f"First text: {first_text}, Second text: {second_text}")