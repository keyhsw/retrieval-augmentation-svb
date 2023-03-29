import streamlit as st
from PIL import Image

from .constants import (QUERIES, PLAIN_GPT_ANS, GPT_WEB_RET_AUG_ANS, GPT_LOCAL_RET_AUG_ANS,
                        BUTTON_LOCAL_RET_AUG, BUTTON_WEB_RET_AUG)


def set_question():
    st.session_state['query'] = st.session_state['q_drop_down']


def set_q1():
    st.session_state['query'] = QUERIES[0]


def set_q2():
    st.session_state['query'] = QUERIES[1]


def set_q3():
    st.session_state['query'] = QUERIES[2]


def set_q4():
    st.session_state['query'] = QUERIES[3]


def set_q5():
    st.session_state['query'] = QUERIES[4]


def main_column():
    placeholder = st.empty()
    with placeholder:
        search_bar, button = st.columns([3, 1])
        with search_bar:
            username = st.text_area(f" ", max_chars=200, key='query')

        with button:
            st.write(" ")
            st.write(" ")
            run_pressed = st.button("Run", key="run")

    st.write(" ")
    st.radio("Answer Type:", (BUTTON_LOCAL_RET_AUG, BUTTON_WEB_RET_AUG), key="query_type")

    # st.sidebar.selectbox(
    #      "Example Questions:",
    #      QUERIES,
    #      key='q_drop_down', on_change=set_question)

    st.markdown(f"<h5> {PLAIN_GPT_ANS} </h5>", unsafe_allow_html=True)
    placeholder_plain_gpt = st.empty()
    st.text(" ")
    st.text(" ")
    if st.session_state.get("query_type", BUTTON_LOCAL_RET_AUG) == BUTTON_WEB_RET_AUG:
        st.markdown(f"<h5> {GPT_LOCAL_RET_AUG_ANS} </h5>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h5>{GPT_WEB_RET_AUG_ANS} </h5>", unsafe_allow_html=True)
    placeholder_retrieval_augmented = st.empty()

    return run_pressed, placeholder_plain_gpt, placeholder_retrieval_augmented


def right_sidebar():
    st.markdown("<h5> Example questions </h5>", unsafe_allow_html=True)
    st.button(QUERIES[0], on_click=set_q1)
    st.button(QUERIES[1], on_click=set_q2)
    st.button(QUERIES[2], on_click=set_q3)
    st.button(QUERIES[3], on_click=set_q4)
    st.button(QUERIES[4], on_click=set_q5)


def left_sidebar():
    with st.sidebar:
        image = Image.open('logo/haystack-logo-colored.png')
        st.markdown("Thank you for visiting this 🤗 space. \n\n"
                    "This is an effort to showcase how to use Haystack for Retrieval-Augmented QA, "
                    "with a local document store as well as a WebRetriever (coming soon!). \n\n"
                    "For more information on how this was built, a repository will be published soon "
                    "containing the instructions and code. We will update the link here.")

        # st.markdown(
        #     "## How to use\n"
        #     "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below\n"
        #     "2. Enter a Serper Dev API key\n"
        #     "3. Enjoy 🤗\n"
        # )

        # api_key_input = st.text_input(
        #     "OpenAI API Key",
        #     type="password",
        #     placeholder="Paste your OpenAI API key here (sk-...)",
        #     help="You can get your API key from https://platform.openai.com/account/api-keys.",
        #     value=st.session_state.get("OPENAI_API_KEY", ""),
        # )

        # if api_key_input:
        #     set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown(
            "## How this works\n"
            "This app was built with [Haystack](https://haystack.deepset.ai) using the"
            " [`PromptNode`](https://docs.haystack.deepset.ai/docs/prompt_node), "
            "[`Retriever`](https://docs.haystack.deepset.ai/docs/retriever#embedding-retrieval-recommended),"
            "and [`FAISSDocumentStore`](https://docs.haystack.deepset.ai/reference/document-store-api#faissdocumentstore)\n\n"
            " You can find the source code in **Files and versions** tab."
        )

        st.markdown("---")
        st.image(image, width=250)
