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

p_1 = None
p_2 = None


def app_init():
    # indexing_pipeline = Pipeline.load_from_yaml("pipeline.yaml", pipeline_name="indexing")
    # file_paths = glob.glob("data/*")
    # ds = indexing_pipeline.get_node("DocumentStore")
    # ds.delete_all_documents()
    # indexing_pipeline.run(file_paths=file_paths)
    # ds.update_embeddings(indexing_pipeline.get_node("Retriever"))
    # ds.save(config_path="my_faiss_config.json", index_path="my_faiss_index.faiss")

    global p_1
    p_1 = Pipeline.load_from_yaml("pipeline.yaml", pipeline_name="query_1")

    global p_2
    p_2 = Pipeline.load_from_yaml("pipeline.yaml", pipeline_name="query_2")


def main():
    app_init()
    st.title("Haystack Demo")
    input = st.text_input("Query ...")

    query_type = st.radio("Type",
                          ("Retrieval Augmented", "Retrieval Augmented with Sources",
                           "Retrieval Augmented with Web Search"))


    col_1, col_2 = st.columns(2)

    with col_1:
        st.text("PLAIN")
        answers = p_1.run(input)["answers"]
        for ans in answers:
            st.text(ans.answer)

    with col_2:
        st.write(query_type.upper())
        answers = p_2.run(input)["answers"]
        for ans in answers:
            st.text(ans.answer)


if __name__ == "__main__":
    main()
