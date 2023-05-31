from settings import OPENAI_API_KEY
import ast

import streamlit as st

from utils import get_products_list
from agents import search_agent
search = st.text_input("Search for product")

if search:
    # list = get_products_list(search)
    # st.table(list)
    agent_chain = search_agent()
    answer = agent_chain.run(input=search)
    # st.write(answer["intermediate_steps"][3])
    products = ast.literal_eval(answer["intermediate_steps"][3])
    print(products)
    st.table([dict(name=item[0], price=item[1], id=item[2], description=item[3]) for item in products])