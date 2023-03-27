import streamlit as st
from backend_utils import app_init, set_q1, set_q2, set_q3, set_q4, set_q5

st.markdown("<center> <h1> Haystack Demo </h1> </center>", unsafe_allow_html=True)

if st.session_state.get('pipelines_loaded', False):
    with st.spinner('Loading pipelines...'):
        p1, p2, p3 = app_init()
        st.success('Pipelines are loaded', icon="✅")
        st.session_state['pipelines_loaded'] = True

placeholder = st.empty()
with placeholder:
    search_bar, button = st.columns([3, 1])
    with search_bar:
        username = st.text_area(f"", max_chars=200, key='query')

    with button:
        st.write("")
        st.write("")
        run_pressed = st.button("Run")

st.radio("Type", ("Retrieval Augmented", "Retrieval Augmented with Web Search"), key="query_type")

# st.sidebar.selectbox(
#      "Example Questions:",
#      QUERIES,
#      key='q_drop_down', on_change=set_question)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.button('Example Q1', on_click=set_q1)
with c2:
    st.button('Example Q2', on_click=set_q2)
with c3:
    st.button('Example Q3', on_click=set_q3)
with c4:
    st.button('Example Q4', on_click=set_q4)
with c5:
    st.button('Example Q5', on_click=set_q5)

st.markdown("<h4> Answer with PLAIN GPT </h4>", unsafe_allow_html=True)
placeholder_plain_gpt = st.empty()
st.text("")
st.text("")
st.markdown(f"<h4> Answer with {st.session_state['query_type'].upper()} </h4>", unsafe_allow_html=True)
placeholder_retrieval_augmented = st.empty()

if st.session_state.get('query') and run_pressed:
    input = st.session_state['query']
    p1, p2, p3 = app_init()
    answers = p1.run(input)
    placeholder_plain_gpt.markdown(answers['results'][0])

    if st.session_state.get("query_type", "Retrieval Augmented") == "Retrieval Augmented":
        answers_2 = p2.run(input)
    else:
        answers_2 = p3.run(input)
    placeholder_retrieval_augmented.markdown(answers_2['results'][0])
