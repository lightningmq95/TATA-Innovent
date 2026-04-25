import fitz  # PyMuPDF
from PIL import Image
import io
import re
from nltk.corpus import stopwords
from collections import defaultdict
import nltk
import streamlit as st
import requests
import json

# Load car manuals from JSON file
with open('manuals.json', 'r') as file:
    carManuals = json.load(file)

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

def extract_keywords(text):
    # Simple keyword extraction by splitting text into words
    words = re.findall(r'\b\w+\b', text)
    
    # Get the list of stopwords
    stop_words = set(stopwords.words('english'))
    
    # Remove stopwords from the list of words
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    return set(filtered_words)

def find_page_with_max_tokens(pdf_path, response_keywords, prompt_keywords):
    # Open the PDF file
    pdf_document = fitz.open(f'manuals/{pdf_path}')
    
    # Initialize a dictionary to keep track of token counts per page
    token_counts = defaultdict(int)

    # Define weights
    weights = {
        'common': 5,
        'NNP': 4,  # Proper noun
        'NN': 3,   # Noun
        'VB': 2,   # Verb
        'JJ': 1    # Adjective
    }

    # Default weight for other POS tags
    default_weight = 0.5
    
    # Find common keywords
    common_keywords = set(response_keywords).intersection(set(prompt_keywords))
 
    # Compile regex patterns for response keywords
    response_patterns = {kw: re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE) for kw in response_keywords}


    # Iterate through each page in the PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        
        # Tokenize and tag the text
        tokens = nltk.word_tokenize(text)
        tagged_tokens = nltk.pos_tag(tokens)

        # Count occurrences of each token on the current page with weights
        for token, tag in tagged_tokens:
            token_lower = token.lower()
            if any(pattern.search(token_lower) for pattern in response_patterns.values()):
                if token_lower in common_keywords:
                    token_counts[page_num] += weights['common']
                elif tag in weights:
                    token_counts[page_num] += weights[tag]
                else:
                    token_counts[page_num] += default_weight
    
    # Find the page with the maximum token occurrences
    max_page = max(token_counts, key=token_counts.get)
    
    # Return the page number (1-based index)
    return max_page + 1

def show_pdf_page(pdf_path, page_number, keywords):
    # Open the PDF file
    doc = fitz.open(f'manuals/{pdf_path}')
    
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
    # st.image(img, caption=f"Page {page_number} of the PDF")
    return img

def extract_pdf_page(pdf_path, prompt, response):
    # Extract keywords from the generated text
    response_keywords = extract_keywords(response)
    prompt_keywords = extract_keywords(prompt)
    print("Response Keywords:", response_keywords)
    print("Prompt Keywords:", prompt_keywords)
    page_no = find_page_with_max_tokens(pdf_path, response_keywords, prompt_keywords)
    return show_pdf_page(pdf_path, page_no, response_keywords)

# Initialize session state for product and chat messages
if 'product' not in st.session_state:
    st.session_state['product'] = ''
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'images' not in st.session_state:
    st.session_state['images'] = []

# # Select box for product selection
# product = st.selectbox("Select a product", list(carManuals.keys()))
# st.session_state['product'] = product

# Select box for product selection (pinned to the sidebar)
product = st.sidebar.selectbox("Select a product", list(carManuals.keys()))
st.session_state['product'] = product

# Chatbox interface
st.write("## Chatbox")


def get_common_words(text1, text2):
    # Tokenize the texts into sets of words
    words1 = set(text1.split())
    words2 = set(text2.split())
    
    # Find the intersection of the two sets
    common_words = words1.intersection(words2)
    
    # Convert the intersection back to a string
    return ' '.join(common_words)


# Display chat messages from history on app rerun
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and i < len(st.session_state['images']):
            if (st.session_state['images'][i] != ""):
                st.image(st.session_state['images'][i], caption=f"Referenced Text")

# React to user input
if prompt := st.chat_input("Enter a prompt"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.images.append("")
    print(len(st.session_state.messages), len(st.session_state.images))

    response = requests.post("http://peaceful-personally-tadpole.ngrok-free.app/generate", json={
        "selected_car": st.session_state['product'], "prompt": prompt})

    if response.status_code == 200:
        response_json = response.json()
        response_text = response_json.get('generated_text', 'No response from API')  # Extract the response text
        rag_text = response_json.get('rag', 'No response from API')
        score = response_json.get('score', "No score")

        # streamlit_text = response_text.split("userPrompt:")[-1].strip().replace("<|begin_of_text|>", "").replace("<|end_of_text|>", "")
        # streamlit_text = f"## Optimized Query:\n{streamlit_text}"
        # response_text = response_text.split("Response:")[-1].strip().replace("<|begin_of_text|>", "").replace("<|end_of_text|>", "")

        user_prompt_text = response_text.split("userPrompt:")[-1].strip().replace("<|begin_of_text|>", "").replace("<|end_of_text|>", "")\
        .split("Response:")[0]
        response_text = response_text.split("Response:")[-1].strip().replace("<|begin_of_text|>", "").replace("<|end_of_text|>", "")

        # Format the streamlit text
        streamlit_text = f"Query score: {score}\n## Optimized Query:\n{user_prompt_text}\n## LLM Response:\n{response_text}\n## RAG Response:\n{rag_text}"


        # # Extract keywords from the generated text
        # response_keywords = extract_keywords(response_text)
        # prompt_keywords = extract_keywords(prompt)

        # Load the correct PDF based on the selected car
        pdf_path = carManuals[st.session_state['product']]
        
        # Find the page with the maximum occurrences of the keywords
        # max_page = find_page_with_max_tokens(pdf_path, response_keywords, prompt_keywords)
        
        # # Show the page with the maximum occurrences of the keywords and highlight them
        # show_pdf_page(pdf_path, max_page, response_keywords)
        # img = extract_pdf_page(pdf_path, prompt, response_text)

        # Get the common words between rag_text and response_text
        # common_text = get_common_words(rag_text, response_text)
        img = extract_pdf_page(pdf_path, prompt, rag_text+response_text)

        with st.chat_message("assistant"):
            # st.markdown(response_text)
            st.markdown(streamlit_text)
            st.image(img, caption=f"Referenced Text")

        # Add assistant response to chat history
        # st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.session_state.messages.append({"role": "assistant", "content": streamlit_text})
        st.session_state.images.append(img)


    else:
        response_text = "Unable to fetch a response"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response_text)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.session_state.images.append("")