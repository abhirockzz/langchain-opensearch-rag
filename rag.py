from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms.bedrock import Bedrock
import boto3
from opensearch_langchain_vector_store import get_vector_store


def create_bedrock_llm(bedrock_client, model_version_id):
    bedrock_llm = Bedrock(
        model_id=model_version_id, 
        client=bedrock_client,
        model_kwargs={'temperature': 0}
        )
    return bedrock_llm

def search(question):
    region = "us-east-1"

    bedrock_client = boto3.client("bedrock-runtime", region_name=region)
    
    bedrock_model_id = "anthropic.claude-v2"

    bedrock_llm = Bedrock(
        model_id=bedrock_model_id, 
        client=bedrock_client,
        model_kwargs={'temperature': 0}
    )

    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. don't include harmful content

    {context}

    Question: {question}
    Answer:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    #print(f"Starting the chain with KNN similarity using OpenSearch")

    qa = RetrievalQA.from_chain_type(llm=bedrock_llm, 
                                     chain_type="stuff", 
                                     retriever=get_vector_store().as_retriever(search_kwargs={'k': 10}),
                                     return_source_documents=True,
                                     chain_type_kwargs={"prompt": PROMPT, "verbose": True},
                                     verbose=True)
    
    response = qa.invoke(question, return_only_outputs=False)
        
    source_documents = response.get('source_documents')
    
    # for d in source_documents:
    #     print(f"With the following similar content from OpenSearch:\n{d.page_content}\n")
    #     print(f"Metadata: {d.metadata}")
    
    flattened_results = [{"content":d.page_content, "metadata":d.metadata} for d in source_documents]

    #print(f"The answer from Bedrock {bedrock_model_id} is: {response.get('result')}")

    return flattened_results, response.get('result')

if __name__ == "__main__":
    search()