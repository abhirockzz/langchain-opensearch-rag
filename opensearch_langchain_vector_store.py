from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import OpenSearchVectorSearch
from opensearchpy import RequestsHttpConnection
from requests_aws4auth import AWS4Auth

import boto3
import os

def get_vector_store():
    
    embeddings = BedrockEmbeddings(model_id = "amazon.titan-embed-text-v1")
    
    service = "aoss"  # must set the service as 'aoss'
    region = "us-east-1"
    opensearch_index_name = os.getenv("opensearch_index_name")
    opensearch_url = os.getenv("opensearch_url"),

    credentials = boto3.Session().get_credentials()

    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    store = OpenSearchVectorSearch(
        embedding_function=embeddings,
        opensearch_url=opensearch_url,
        index_name=opensearch_index_name,
        engine=os.getenv("engine"),
        http_auth=awsauth,
        timeout=300,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )

    return store