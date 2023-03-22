import glob
import os
import logging
import sys

import streamlit as st
from haystack import Pipeline
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import Shaper, PromptNode, PromptTemplate, PromptModel
from haystack.nodes.retriever.web import WebRetriever
from haystack.schema import Document

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(asctime)s %(name)s:%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

p_1 = None
p_2 = None


def get_plain_pipeline():
    prompt_open_ai = PromptModel(model_name_or_path="text-davinci-003", api_key=api_key)

    # Now let make one PromptNode use the default model and the other one the OpenAI model:
    plain_llm_template = PromptTemplate(name="plain_llm", prompt_text="Answer the following question: $query")
    node_openai = PromptNode(prompt_open_ai, default_prompt_template=plain_llm_template, max_length=300)

    pipeline = Pipeline()
    pipeline.add_node(component=node_openai, name="prompt_node", inputs=["Query"])
    return pipeline


def get_ret_aug_pipeline():
    ds = FAISSDocumentStore(faiss_index_path="my_faiss_index.faiss",
                            faiss_config_path="my_faiss_index.json")

    retriever = EmbeddingRetriever(
        document_store=ds,
        embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
        model_format="sentence_transformers",
        top_k=2
    )
    shaper = Shaper(func="join_documents", inputs={"documents": "documents"}, outputs=["documents"])

    default_template= PromptTemplate(
        name="question-answering",
        prompt_text="Given the context please answer the question. Context: $documents; Question: "
                    "$query; Answer:",
    )
    # Let's initiate the PromptNode
    node = PromptNode("text-davinci-003", default_prompt_template=default_template, api_key=api_key, max_length=500)

    # Let's create a pipeline with Shaper and PromptNode
    pipe = Pipeline()
    pipe.add_node(component=retriever, name='retriever', inputs=['Query'])
    pipe.add_node(component=shaper, name="shaper", inputs=["retriever"])
    pipe.add_node(component=node, name="prompt_node", inputs=["shaper"])
    return pipe


def app_init():

    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    p1 = get_plain_pipeline()
    p2 = get_ret_aug_pipeline()
    return p1, p2


def main():
    p1, p2 = app_init()
    st.title("Haystack Demo")
    input = st.text_input("Query ...")

    query_type = st.radio("Type",
                          ("Retrieval Augmented", "Retrieval Augmented with Web Search"))
    col_1, col_2 = st.columns(2)

    with col_1:
        st.text("PLAIN")
        answers = p1.run(input)["answers"]
        for ans in answers:
            st.text(ans.answer)

    with col_2:
        st.write(query_type.upper())
        answers = p2.run(input)["answers"]
        for ans in answers:
            st.text(ans.answer)


if __name__ == "__main__":
    main()
