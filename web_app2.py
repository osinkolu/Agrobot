import streamlit as st
my_page = st.sidebar.radio('Page Navigation', ['page 1', 'page 2'])

if my_page == 'page 1':
    st.title('here is a page')
    button = st.button('a button')
    if button:
        st.write('clicked')
else:
    st.title('this is a different page')
    slide = st.slider('this is a slider')
    slide