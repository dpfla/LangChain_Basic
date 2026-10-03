#from langchain_ollama import ChatOllama
#from langchain_core.prompts import PromptTemplate
#from langchain_core.output_parsers import StrOutputParser
#
#prompt_template = PromptTemplate(
#    template="what is the capital of {country}? Return the name of the capital only.",
#    input_variables=["country"]
#)
#
#
#prompt = prompt_template.invoke({"country": "France"})
#
#llm = ChatOllama(model="qwen3.5:2b")
#
#response = llm.invoke(prompt)
#
#output_parser = StrOutputParser()
#parsed_response = output_parser.invoke(response)
#
#print(parsed_response)


from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


class Capital(BaseModel):
    capital: str = Field(description="The name of the capital")
    population: int = Field(description="The population of the capital")
    area: float = Field(description="The area of the capital")
    language: str = Field(description="The language of the capital")

prompt_template = PromptTemplate(
    template="what is the capital of {country}? Return the name of the capital only.",
    input_variables=["country"]
)


prompt = prompt_template.invoke({"country": "France"})

llm = ChatOllama(model="qwen3.5:2b")

response = llm.with_structured_output(Capital).invoke(prompt)

print(response.capital)
print(response.population)
print(response.area)
print(response.language)

print(response.model_dump())
print(response.model_dump_json())
