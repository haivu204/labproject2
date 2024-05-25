import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import streamlit as st
import threading
import time


if not firebase_admin._apps:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("firebasekey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def flatten_dict(original_dict, name):
    flattened_dict = {}
    for key, nested_dict in original_dict.items():

        for nested_key, value in nested_dict.items():
            if nested_key == name:
                new_key = key[4:]
                flattened_dict[new_key] = value
    return flattened_dict




# Function to fetch data from Firestore
# def fetch_firestore_data(collection_name, document_name):
#     doc_ref = db.collection(collection_name).document(document_name)
#     doc = doc_ref.get()
#     if doc.exists:
#         data = doc.to_dict()
#         return data
#     else:
#         return None


# Streamlit app

def fetch_firestore_data(collection_name, document_name):
    doc_ref = db.collection(collection_name).document(document_name)

    return doc_ref

def main():
    while 1:
        st.header("SINH VIEN NGHIEN CUU KHOA HOC-DH BKHN")

        doc_ref0 = db.collection('haidata').document('realtime')
        doc0 = doc_ref0.get()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Tempurature", value=int(doc0.get("nhietdo1")), delta=1)
        col2.metric(label="Huminity", value=int(doc0.get("doam1")), delta=1)
        col3.metric(label="CO2", value=int(doc0.get("co21")), delta=1)
        col4.metric(label="Current", value=int(doc0.get("dongdien")), delta=1)



        doc_ref = db.collection('haidata').document('test_document')
        doc = doc_ref.get()
        tem = {}

        # Check if the document exists
        if doc.exists:
            # Get the data from the document
            data = doc.to_dict()
            # Extract the first 100 fields
            first_100_fields = {key: data[key] for idx, key in enumerate(data.keys()) if idx < 100}
            tem = flatten_dict(first_100_fields, 'nhietdo')
            print(tem)
            print("First 100 fields:")
            print(first_100_fields)
        else:
            print(u'No such document!')

    # df = pd.DataFrame(data.items(), columns=)

    # Display data in a table
        st.write("Data:")
        df = pd.DataFrame(first_100_fields)

        st.write(df)


        # Plot the temperature data
        # st.subheader("TEMPERATURE")
        #
        # st.line_chart(tem, color = "#ffaa00" )

        df2 = pd.DataFrame.from_dict(first_100_fields, orient= 'index')
        st.line_chart(df2)
        if "last_update" not in st.session_state:
            st.session_state.last_update = time.time()

        if time.time() - st.session_state.last_update >= 10:
            st.session_state.last_update = time.time()

            # Schedule the callback to run every minute
        st.query_params.update(__callback=main)

        co2 = st.slider("nong do CO2 (ppm)", 488, 8000)
        tem = st.slider("nhiet do phong (do c)", 15, 30)
        col1, col2, col3, col4 = st.columns(4)

        Fan = col1.button("FAN")
        Cooling = col2.button("COOLING")
        Stop = col3.button("STOP")

        data = {
            "co2": co2,
            "tem": tem,
            "Fan": Fan,
            "Cooling": Cooling,
            "Stop": Stop
        }
       

                # Create a document in Firestore
        doc_ref = db.collection('haidata').document('control')
        doc_ref.set(data)
        time.sleep(1)
        st.rerun()
if __name__ == "__main__":
    main()




