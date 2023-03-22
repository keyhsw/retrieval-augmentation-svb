import sys
import logging
import streamlit as st
import haystack

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(asctime)s %(name)s:%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)


st.title("Haystack Demo")
st.text_input("Query ...")
st.text(haystack.__version__)
