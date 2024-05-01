import streamlit as st
from google.cloud import firestore

db = firestore.Client.from_service_account_json("firebasekey.json")

# Create a reference to the Google post.
doc_ref = db.collection("dungdata").document("realtime")
    # Then get the data at that reference.
doc = doc_ref.get()


def update_dashboard():
    while True:
        doc_ref = db.collection("haidata").document("realtime")
        doc = doc_ref.get()
        col1, col2, col3 = st.columns(3)
        col2.metric("Wind", "9 mph", "-8%")
        col3.metric("Humidity", "74" , "4%")
        col1.metric(label="Tempurature", value= int(doc.get("nhietdo1")), delta = 1)
        submit = st.button("Turn fan on")



st.title("Air quality measuring")

with st.empty():
    update_dashboard()
