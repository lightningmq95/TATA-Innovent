import fitz  # PyMuPDF
from PIL import Image
import io
import re
from nltk.corpus import stopwords
import nltk
import streamlit as st
import requests

# Mapping of car names to their respective PDF paths
car_manuals = {
    "Tata Punch": "manuals/punch.pdf",
    "Tata Sumo Gold": "manuals/sumo_gold.pdf",
}

def extract_keywords(text):
    # Simple keyword extraction by splitting text into words
    words = re.findall(r'\b\w+\b', text)
    
    # Get the list of stopwords
    stop_words = set(stopwords.words('english'))
    
    # Remove stopwords from the list of words
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    return set(filtered_words)

def find_page_with_max_tokens(pdf_path, tokens):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Initialize a dictionary to keep track of token counts per page
    token_counts = {}
    
    # Iterate through each page in the PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        
        # Count occurrences of each token on the current page
        count = sum(text.lower().count(token.lower()) for token in tokens)
        
        # Store the count in the dictionary
        token_counts[page_num] = count
    
    # Find the page with the maximum token occurrences
    max_page = max(token_counts, key=token_counts.get)
    
    # Return the page number (1-based index)
    return max_page + 1

def show_pdf_page(pdf_path, page_number, keywords):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Load the specified page (0-based index)
    page = doc.load_page(page_number - 1)
    
    # Highlight the keywords on the page
    for keyword in keywords:
        text_instances = page.search_for(keyword)
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.update()
    
    # Convert the page to an image
    pix = page.get_pixmap()
    img = Image.open(io.BytesIO(pix.tobytes()))
    
    # Display the image in Streamlit
    st.image(img, caption=f"Page {page_number} of the PDF")

# Streamlit UI
st.title("Car Prompt Submission")
selected_car = st.selectbox("Select a car", list(car_manuals.keys()))
prompt = st.text_input("Enter your prompt")

if st.button("Submit"):
    # Send selected_car and prompt separately in the JSON payload
    response = requests.post(
        'http://peaceful-personally-tadpole.ngrok-free.app/generate',
        json={"selected_car": selected_car, "prompt": prompt}
    )
    
    if response.status_code == 200:
        generated_text = response.json().get("generated_text", "") #gets raw response from model
        #from the raw response strips off all the data from the point userPrompt and replaces bot and eot
        streamlit_text = generated_text.split("userPrompt:")[-1].strip().replace("<|begin_of_text|>", "").replace("<|end_of_text|>", "")
        st.success("Prompt submitted successfully!")
        st.markdown("<h1 style='font-size:23px;'>Optimized Query:</h1>", unsafe_allow_html=True)
        #from the raw response of the model strips off everything from the point Response such that only the text after that is feeded to show pdf page fucntion
        pdf_relevant_response = generated_text.split("Response:")[-1].strip().replace("<|end_of_text|>", "")
        st.write(streamlit_text)
        
        # Extract keywords from the generated text
        keywords = extract_keywords(pdf_relevant_response)
        print(keywords)
        
        # Load the correct PDF based on the selected car
        pdf_path = car_manuals[selected_car]
        
        # Find the page with the maximum occurrences of the keywords
        max_page = find_page_with_max_tokens(pdf_path, keywords)
        
        # Show the page with the maximum occurrences of the keywords and highlight them
        show_pdf_page(pdf_path, max_page, keywords)
    else:
        st.error("Failed to submit prompt.")