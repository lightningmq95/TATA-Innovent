# import streamlit as st
# import requests

# # Streamlit UI
# st.title("Car Prompt Submission")
# selected_car = st.selectbox("Select a car", ["Tata Punch", "Maruti Swift", "Hyundai i20"])
# prompt = st.text_input("Enter your prompt")

# if st.button("Submit"):
#     concatenated_prompt = f"In {selected_car}, {prompt}"
#     response = requests.post("https://peaceful-personally-tadpole.ngrok-free.app/submit-prompt", json={"prompt": concatenated_prompt})
#     if response.status_code == 200:
#         st.success("Prompt submitted successfully!")
#     else:
#         st.error("Failed to submit prompt.")

import streamlit as st
import requests

# Streamlit UI
st.title("Car Prompt Submission")
selected_car = st.selectbox("Select a car", ["Tata Punch", "Tata Sumo Gold", "Hyundai i20"])
prompt = st.text_input("Enter your prompt")

if st.button("Submit"):
    concatenated_prompt = f"In {selected_car}, {prompt}"
    response = requests.post('http://peaceful-personally-tadpole.ngrok-free.app/generate', json={"prompt": concatenated_prompt})
    
    if response.status_code == 200:
        generated_text = response.json().get("generated_text", "")
        st.success("Prompt submitted successfully!")
        st.write("Generated Response:")
        st.write(generated_text)
    else:
        st.error("Failed to submit prompt.")