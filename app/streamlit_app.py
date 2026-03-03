import streamlit as st
import requests
import json

st.set_page_config(page_title="User Support Agent", layout="centered")

st.title("User Support Agent")

# Sidebar placeholder (will be filled after response)
st.sidebar.title("Advanced Details")

user_input = st.text_area("Ask something")

if st.button("Send"):
    if user_input.strip() != "":
        with st.spinner("Thinking..."):
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"message": user_input}
            )
            
            #st.write("Status Code:", response.status_code)
            #st.write("Raw Response:", response.text)

            data = response.json()

            persona = json.loads(data["persona"])

            st.markdown("Detected Persona")
            st.success(persona["persona"])

            st.markdown("Response")
            st.write(data["response"])

            
            st.sidebar.markdown("### Sentiment Analysis")
            st.sidebar.write("Sentiment:", data["sentiment"]["label"])
            st.sidebar.write("Confidence:", round(data["sentiment"]["confidence"], 3))