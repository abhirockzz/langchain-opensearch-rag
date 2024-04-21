from langchain_community.embeddings import BedrockEmbeddings
from opensearch_langchain_vector_store import get_vector_store
import os

def search(question):

    results = get_vector_store().similarity_search_with_score(
       question,
        #search_type="script_scoring",
        space_type="l2",
        vector_field=os.getenv("vector_field"),
        text_field=os.getenv("text_field"),
        metadata_field=os.getenv("metadata_field"),
    )

    # for doc, score in results:
    #     print("======")
    #     print("Score: ", score)
    #     print("meta: ", doc.metadata)
    #     print(doc.page_content)
    #     print("======-")
    
    #flatten results for easier display and handling
    flattened_results = [{"content":res[0].page_content, "score":res[1], "metadata":res[0].metadata} for res in results] 

    return flattened_results


def get_embedding(text):
    embeddings = BedrockEmbeddings()
    
    return embeddings.embed_query(text)

def main():
    #get_similarity_search_results("What is Amazon's doing in the field of generative AI?")
    search("What were the key challenges Amazon faced in 2022?")
if __name__ == "__main__":
    main()