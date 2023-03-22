import glob
import logging
import sys

import streamlit as st
from haystack import Pipeline

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(asctime)s %(name)s:%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

p = None


def app_init():
    indexing_pipeline = Pipeline.load_from_yaml("pipeline.yaml", pipeline_name="indexing")
    file_paths = glob.glob("data/*")
    ds = indexing_pipeline.get_node("DocumentStore")
    ds.delete_all_documents()
    indexing_pipeline.run(file_paths=file_paths)
    ds.update_embeddings(indexing_pipeline.get_node("Retriever"))
    ds.save(config_path="my_faiss_config.json", index_path="my_faiss_index.faiss")

    global p
    p = Pipeline.load_from_yaml("pipeline.yaml", pipeline_name="query")


def main():
    app_init()
    st.title("Haystack Demo")
    input = st.text_input("Query ...")
    st.text(p.run(str(input or "test")))


if __name__ == "__main__":
    main()
