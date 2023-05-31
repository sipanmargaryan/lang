from settings import OPENAI_API_KEY
import ast

import streamlit as st

from utils import get_products_list
from agents import search_agent
search = st.text_input("Search for product")

if search:
    agent_chain = search_agent()
    answer = agent_chain.run(input=search)
    products = ast.literal_eval(answer["intermediate_steps"][3])
    st.table([dict(name=item[0], price=item[1], id=item[2], description=item[3]) for item in products])