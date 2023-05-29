from settings import OPENAI_API_KEY

import streamlit as st

from utils import get_products_list
search = st.text_input("Search for product")

if search:
    list = get_products_list(search)
    st.table(list)