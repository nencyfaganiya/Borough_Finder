import pandas as pd
import requests
import streamlit as st

# Function to fetch borough for a single postcode
def get_borough(postcode):
    url = f"https://api.postcodes.io/postcodes/{postcode}/validate"
    validate_response = requests.get(url)
    
    # Check if the postcode is valid
    if validate_response.status_code == 200 and validate_response.json().get("result", False):
        # If valid, fetch the borough
        lookup_url = f"https://api.postcodes.io/postcodes/{postcode}"
        lookup_response = requests.get(lookup_url)
        if lookup_response.status_code == 200:
            data = lookup_response.json()
            if "result" in data and data["result"]:
                return data["result"].get("admin_district", "Unknown")
    # Return empty for invalid postcodes
    return ""

# Streamlit app
st.title("Borough Finder")

# Input field for the user to enter postcodes (one per line)
input_postcodes = st.text_area("Enter postcodes (one per line)")

# Button to process the postcodes
if st.button("Find Boroughs"):
    # Split the input by newlines and strip any extra spaces
    postcodes = [postcode.strip() for postcode in input_postcodes.split("\n")]

    # Create a DataFrame with postcodes and their corresponding boroughs
    boroughs = [get_borough(postcode.replace(" ", "")) for postcode in postcodes]
    result_df = pd.DataFrame({"Postcode": postcodes, "Borough": boroughs})

# Adjust the width of the "Borough" column
    st.write("Results:")
    st.dataframe(result_df.style.set_table_styles(
        [{'selector': 'td.col1', 'props': [('width', '200px')]}]  # Adjust width for "Postcode" column (col0)
    ).set_table_styles(
        [{'selector': 'td.col2', 'props': [('width', '340px')]}]  # Adjust width for "Borough" column (col1)
    ))

    # Option to copy the results
    st.text("You can copy the table above.")
