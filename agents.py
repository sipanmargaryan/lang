from langchain import LLMChain, OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.agents import AgentExecutor, ConversationalAgent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from database import DATABASE_URL

db = SQLDatabase.from_uri(DATABASE_URL)
llm = OpenAI(temperature=0, verbose=True)
sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_intermediate_steps=True)

sql_tool = Tool(
    name='Products DB',
    func=sql_chain,
    description="Useful for when you need to get list of  products or shopping card " \
                "or add something into shopping card .",
    return_direct = True
    
)


prefix = """You are assistant which chats with users answering as short as possible. Note that your information is not up to date and you must access to another tools to have information after 2020.don't make search in memory hostory. Make sure you include only necessary information, answer the questions as best as you can and to answer properly you have to access to this tools if needed:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

tools = [sql_tool]
    
prompt = ConversationalAgent.create_prompt(
    tools, 
    prefix=prefix, 
    suffix=suffix, 
    input_variables=["input", "chat_history", "agent_scratchpad"]
)
llm_chain = LLMChain(llm=ChatOpenAI(temperature=0), prompt=prompt)



def search_agent():
    memory = ConversationBufferMemory(memory_key="chat_history")
    
    
    agent = ConversationalAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)
    