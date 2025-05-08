import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timezone
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def main():
    # Load MongoDB credentials from environment
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")
    collection_name = os.getenv("MONGO_COLLECTION_NAME")

    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Display title
    st.title("Order Creation Form")

    # Form elements
    with st.form(key='user_form'):
        name = st.text_input("Enter your full name", placeholder="name")
        company_name = st.text_input("Enter the company name", placeholder="company name")
        email = st.text_input("Enter your email", placeholder="email")
        part_no = st.text_input("Enter the part number", placeholder="part number")
        quantity = st.text_input("Enter the quantity", placeholder="quantity")

        submit_button = st.form_submit_button("Create")

        if submit_button:
            # Input validations
            if not name.strip():
                st.error("Name is required.")
            elif not company_name.strip():
                st.error("Company name is required.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            elif not part_no.isalnum():
                st.error("Part number must be alphanumeric.")
            elif not quantity.isdigit():
                st.error("Quantity must be a whole number.")
            else:
                # Prepare and insert data
                data = {
                    "name": name.strip(),
                    "company_name": company_name.strip(),
                    "email": email.strip(),
                    "part_no": part_no.strip(),
                    "quantity": int(quantity),
                    "order_datetime": datetime.now(timezone.utc)
                }

                collection.insert_one(data)

                st.success(
                    f"✅ Data saved! Thanks, **{name}**. We'll contact you at **{email}**. You entered part number: **{part_no}**."
                )

if __name__ == "__main__":
    main()
