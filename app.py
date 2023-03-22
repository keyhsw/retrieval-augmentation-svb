import logging
import sys

import streamlit as st
from haystack import Document
from haystack import Pipeline
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.nodes import FARMReader

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(asctime)s %(name)s:%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

p = None

def app_init():
    docs = [Document(id='1', content='His name is John.'),
            Document(id='2', content='Her name is Jane.'),
            Document(id='3', content='My name is Haystack.')]
    ds = InMemoryDocumentStore()
    ds.write_documents(docs)
    retriever = EmbeddingRetriever(
        document_store=ds,
        embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
        model_format="sentence_transformers",
    )
    ds.update_embeddings(retriever)
    reader = FARMReader("deepset/minilm-uncased-squad2", use_gpu=False)
    p = Pipeline()
    p.add_node(component=retriever, name='retriever', inputs=['Query'])
    p.add_node(component=reader, name='reader', inputs=['retriever'])


def main():
    app_init()
    st.title("Haystack Demo")
    input = st.text_input("Query ...")
    st.text(p.run(input))

if __name__ == "__main__":
    main()