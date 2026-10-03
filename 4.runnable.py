from typing import Any


from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

prompt_template = PromptTemplate(
    template="what is the capital of {country}? Return the name of the capital only.",
    input_variables=["country"]
)


llm = ChatOllama(model="qwen3.5:2b")

output_parser = StrOutputParser()

capital_chain = prompt_template | llm | output_parser

#parsed_response = output_parser.invoke(llm.invoke(prompt_template.invoke({"country": "France"})))
#parsed_response = capital_chain.invoke({"country": "France"})

country_prompt = PromptTemplate(
    template="""Guess the name of country in the {continent} based on the following information:
    {information}
    Return the name of the capital only
    """,
    input_variables=["information", "continent"]
)

country_chain = country_prompt | llm | output_parser
country_response = country_chain.invoke({"information" : "This country is very famous for its wine in Europs"})
print(country_response)

#final_chain = {"country": country_chain} | capital_chain
#final_response = final_chain.invoke({"information" : "This country is very famous for its wine in Europs"})

final_chain = {"information" : RunnablePassthrough(), "continent" : RunnablePassthrough()} | {"country": country_chain} | capital_chain
final_response = final_chain.invoke({"information": "This country is very famous for its wine in Europs", "continent": "Europs"})
print(final_response)