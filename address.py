import re
import spacy
import pymongo

# Load the spaCy model for named entity recognition
nlp = spacy.load("en_core_web_sm")

# Connect to MongoDB (adjust connection string if necessary)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["address_db"]  # Create or use the database
collection = db["user_details"]  # Create or use the collection

# Function to extract details
def extract_details(address_str):
    # NLP Named Entity Recognition (NER)
    doc = nlp(address_str)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Regex patterns
    phone_pattern = r"\+?\d{1,4}[\s\-]?\(?\d{1,3}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{1,4}"
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    street_pattern = r"\d+\s[A-Za-z\s]+(?:[A-Za-z]+)"  # A basic pattern to capture street address

    # Search for patterns in the address string using regex
    phone = re.search(phone_pattern, address_str)
    email = re.search(email_pattern, address_str)
    street = re.search(street_pattern, address_str)

    # Return extracted values
    return {
        "name": name if name else "N/A",
        "phone": phone.group(0) if phone else "N/A",
        "email": email.group(0) if email else "N/A",
        "street": street.group(0) if street else "N/A"
    }

# Function to store the extracted data in MongoDB
def store_in_mongodb(data):
    collection.insert_one(data)
    print("Data stored in MongoDB successfully.")

# Example usage
address_str = "John Doe, 1234 Elm Street, Springfield, +123-456-7890, john.doe@example.com"
extracted_data = extract_details(address_str)
store_in_mongodb(extracted_data)

# Output extracted data
print("Extracted data:", extracted_data)