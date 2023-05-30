import ast
from typing import Dict, List

from langchain import OpenAI, PromptTemplate, SQLDatabase, SQLDatabaseChain

from database import DATABASE_URL
from settings import OPENAI_API_KEY

db = SQLDatabase.from_uri(DATABASE_URL)
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, verbose=True)



db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_intermediate_steps=True)

def get_products_list(query: str) -> List[Dict]:
    template = """
    {product}. for products search data in name, description and price fields. return all fields from products table
    """
    prompt = PromptTemplate(
        input_variables=["product"],
        template=template,
    )
    query = prompt.format(product=query)
    sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_intermediate_steps=True)
    response = sql_chain(query)
    products = ast.literal_eval(response["intermediate_steps"][3])
    return [dict(name=item[0], price=item[1], id=item[2], description=item[3]) for item in products]
