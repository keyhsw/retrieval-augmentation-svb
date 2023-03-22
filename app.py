import sys
import logging
import streamlit as st

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(asctime)s %(name)s:%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)


st.set_page_config(page_title="Haystack Demo")