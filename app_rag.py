import streamlit as st
import rag
from dotenv import load_dotenv

# Load environment variables at the start
load_dotenv()

st.set_page_config(page_title="RAG with OpenSearch and LangChain", layout="wide")
st.title("RAG with OpenSearch and LangChain") #page title


input_text = st.text_input("Ask a question:")
go_button = st.button("Go", type="primary")

if go_button:
    
    with st.spinner("Working..."):
        semantic_results, rag_result = rag.search(question=input_text)

        st.text_area(label="Response:", value=rag_result, height=350)

        with st.expander("Semantic Search results:"):
            st.table(semantic_results)

        # st.write("Semantic Search results:")
        # st.table(semantic_results)