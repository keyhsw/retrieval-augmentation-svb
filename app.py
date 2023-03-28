import streamlit as st
from backend_utils import (get_plain_pipeline, get_retrieval_augmented_pipeline,
                           get_web_retrieval_augmented_pipeline, set_q1, set_q2, set_q3, set_q4, set_q5, QUERIES)

st.set_page_config(
    page_title="Retrieval Augmentation with Haystack",
)

st.markdown("<center> <h2> Reduce Hallucinations with Retrieval Augmentation </h2> </center>", unsafe_allow_html=True)

st.markdown("Ask a question about the collapse of the Silicon Valley Bank (SVB).", unsafe_allow_html=True)

# if not st.session_state.get('pipelines_loaded', False):
#     with st.spinner('Loading pipelines... \n This may take a few mins and might also fail if OpenAI API server is down.'):
#         p1, p2, p3 = app_init()
#         st.success('Pipelines are loaded', icon="✅")
#         st.session_state['pipelines_loaded'] = True

placeholder = st.empty()
with placeholder:
    search_bar, button = st.columns([3, 1])
    with search_bar:
        username = st.text_area(f" ", max_chars=200, key='query')

    with button:
        st.write(" ")
        st.write(" ")
        run_pressed = st.button("Run")

st.markdown("<center> <h5> Example questions </h5> </center>", unsafe_allow_html=True)

st.write(" ")
st.write(" ")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.button(QUERIES[0], on_click=set_q1)
with c2:
    st.button(QUERIES[1], on_click=set_q2)
with c3:
    st.button(QUERIES[2], on_click=set_q3)
with c4:
    st.button(QUERIES[3], on_click=set_q4)
with c5:
    st.button(QUERIES[4], on_click=set_q5)

st.write(" ")
st.radio("Answer Type:", ("Retrieval Augmented (Static news dataset)", "Retrieval Augmented with Web Search"), key="query_type")

# st.sidebar.selectbox(
#      "Example Questions:",
#      QUERIES,
#      key='q_drop_down', on_change=set_question)

st.markdown("<h5> Answer with GPT's Internal Knowledge </h5>", unsafe_allow_html=True)
placeholder_plain_gpt = st.empty()
st.text(" ")
st.text(" ")
st.markdown(f"<h5> Answer with {st.session_state['query_type']} </h5>", unsafe_allow_html=True)
placeholder_retrieval_augmented = st.empty()

if st.session_state.get('query') and run_pressed:
    input = st.session_state['query']
    with st.spinner('Loading pipelines... \n This may take a few mins and might also fail if OpenAI API server is down.'):
        p1 = get_plain_pipeline()
    with st.spinner('Fetching answers from GPT\'s internal knowledge... '
                    '\n This may take a few mins and might also fail if OpenAI API server is down.'):
        answers = p1.run(input)
    placeholder_plain_gpt.markdown(answers['results'][0])

    if st.session_state.get("query_type", "Retrieval Augmented") == "Retrieval Augmented":
        with st.spinner(
                'Loading Retrieval Augmented pipeline... \
                n This may take a few mins and might also fail if OpenAI API server is down.'):
            p2 = get_retrieval_augmented_pipeline()
        with st.spinner('Fetching relevant documents from documented stores and calculating answers... '
                        '\n This may take a few mins and might also fail if OpenAI API server is down.'):
            answers_2 = p2.run(input)
    else:
        p3 = get_web_retrieval_augmented_pipeline()
        answers_2 = p3.run(input)
    placeholder_retrieval_augmented.markdown(answers_2['results'][0])
