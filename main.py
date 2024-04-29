import streamlit as st
from google.cloud import firestore

# Authenticate to Firestore with the JSON account key
import threading
import time
import queue

from google.oauth2 import service_account

q = queue.Queue()

####
# import json
#
# key_dict = json.loads(st.secrets["textkey"])
# creds = service_account.Credentials.from_service_account_info(key_dict)
# db = firestore.Client(credentials=creds, project="Lab Project")

####

db = firestore.Client.from_service_account_json("firebasekey.json")

# Create a reference to the Google post.
doc_ref = db.collection("dungdata").document("realtime")
    # Then get the data at that reference.
doc = doc_ref.get()

# st.metric(label = "Huminity", value = "68", delta = "1")
#
# # Let's see what we got!
# st.write("The id is: ", doc.id)
# st.write("The contents are: ", doc.to_dict())
# time.sleep(1)



q = queue.Queue()

def test_run():
    while True:
        doc_ref = db.collection("haidata").document("realtime")
        doc = doc_ref.get()
        e = int(doc.get("nhietdo1"))
        val = e

        q.put(val)
        print(val)
        time.sleep(1)

def update_dashboard():
    while True:
        col1, col2, col3 = st.columns(3)
        col2.metric("Wind", "9 mph", "-8%")
        col3.metric("Humidity", "74" , "4%")
        val= q.get()

        col1.metric(label="Tempurature", value= int(val), delta = 1)


threading.Thread(target=test_run).start()

# Dashboard title
st.title("Air quality measuring")

with st.empty():
    update_dashboard()
