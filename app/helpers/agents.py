import ast
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain, PromptTemplate
from typing import List
from app.settings import OPENAI_API_KEY
from .database import DATABASE_URL
from app.routers.products.schema import Product




db = SQLDatabase.from_uri(DATABASE_URL)
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, verbose=True)



db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_intermediate_steps=True)

def get_products_list(query: str) -> List[Product]:
    template = """
    Get name, description, price fields from product list which name or description contains {product}
    """
    prompt = PromptTemplate(
        input_variables=["product"],
        template=template,
    )
    query = prompt.format(product=query)
    sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_intermediate_steps=True)
    response = sql_chain(query)
    products = ast.literal_eval(response["intermediate_steps"][3])
    return [Product(name=item[0], description=item[1], price=item[2]) for item in products]