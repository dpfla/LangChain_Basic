#from langchain_ollama import ChatOllama
#from langchain_core.prompts import PromptTemplate
#
#prompt_template = PromptTemplate(
#    template="what is the capital of {country}?",
#    input_variables=["country"]
#)
#
#prompt = prompt_template.invoke({"country": "France"})
#
#llm = ChatOllama(model="qwen3.5:2b")
#
#response = llm.invoke(prompt)
#
#print(response.content)


from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="qwen3.5:2b")

response = llm.invoke([HumanMessage(content="What is the capital of France?")])

print(response.content)