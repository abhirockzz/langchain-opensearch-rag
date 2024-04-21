import streamlit as st
import semantic
from dotenv import load_dotenv

# Load environment variables at the start
load_dotenv()

st.set_page_config(page_title="Semantic Search with OpenSearch and LangChain", layout="wide")
st.title("Semantic Search with OpenSearch and LangChain") #page title


input_text = st.text_input("Ask a question:")
go_button = st.button("Go", type="primary")

if go_button:
    
    with st.spinner("Working..."):
        response_content = semantic.search(question=input_text)
        
        st.table(response_content) #using table so text will wrap
        
        raw_embedding = semantic.get_embedding(input_text)
        
        with st.expander("View question embedding"):
            st.json(raw_embedding)