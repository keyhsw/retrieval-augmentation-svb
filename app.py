import streamlit as st
from utils.backend import (get_plain_pipeline, get_retrieval_augmented_pipeline,
                           get_web_retrieval_augmented_pipeline)
from utils.ui import set_q1, set_q2, set_q3, set_q4, set_q5, left_sidebar, right_sidebar, main_column
from utils.constants import (QUERIES, PLAIN_GPT_ANS, GPT_WEB_RET_AUG_ANS, GPT_LOCAL_RET_AUG_ANS,
                             BUTTON_LOCAL_RET_AUG, BUTTON_WEB_RET_AUG)

st.set_page_config(
    page_title="Retrieval Augmentation with Haystack",
    layout="wide"
)
left_sidebar()

st.markdown("<center> <h2> Reduce Hallucinations with Retrieval Augmentation </h2> </center>", unsafe_allow_html=True)

st.markdown("Ask a question about the collapse of the Silicon Valley Bank (SVB).", unsafe_allow_html=True)

col_1, col_2 = st.columns([4, 2], gap="small")
with col_1:
    run_pressed, placeholder_plain_gpt, placeholder_retrieval_augmented = main_column()

with col_2:
    right_sidebar()

if st.session_state.get('query') and run_pressed:
    ip = st.session_state['query']
    with st.spinner('Loading pipelines... \n This may take a few mins and might also fail if OpenAI API server is down.'):
        p1 = get_plain_pipeline()
    with st.spinner('Fetching answers from plain GPT... '
                    '\n This may take a few mins and might also fail if OpenAI API server is down.'):
        answers = p1.run(ip)
    placeholder_plain_gpt.markdown(answers['results'][0])

    if st.session_state.get("query_type", BUTTON_LOCAL_RET_AUG) == BUTTON_LOCAL_RET_AUG:
        with st.spinner(
                'Loading Retrieval Augmented pipeline that can fetch relevant documents from local data store... '
                '\n This may take a few mins and might also fail if OpenAI API server is down.'):
            p2 = get_retrieval_augmented_pipeline()
        with st.spinner('Getting relevant documents from documented stores and calculating answers... '
                        '\n This may take a few mins and might also fail if OpenAI API server is down.'):
            answers_2 = p2.run(ip)
    else:
        with st.spinner(
                'Loading Retrieval Augmented pipeline that can fetch relevant documents from the web... \
                n This may take a few mins and might also fail if OpenAI API server is down.'):
            p3 = get_web_retrieval_augmented_pipeline()
        with st.spinner('Getting relevant documents from the Web and calculating answers... '
                        '\n This may take a few mins and might also fail if OpenAI API server is down.'):
            answers_2 = p3.run(ip)
    placeholder_retrieval_augmented.markdown(answers_2['results'][0])
