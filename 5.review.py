from typing import final
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="qwen3.5:2b",reasoning=False)
output_parser = StrOutputParser()

food_prompt = PromptTemplate(
    template="what is one of the most popular food in {country}? Please return the name of the food only",
    input_variables=["country"]
)
food_chain = food_prompt | llm | output_parser
#food_response = food_chain.invoke({"country": "South Korea"})
#print(food_response)

recipe_prompt = ChatPromptTemplate.from_messages([
    ("system", "Provide a short recipe. List main ingredients and at most 5 steps."),
    ("human", "Can you give me the recipe for making {food}?")
])
recipe_chain = recipe_prompt | llm | output_parser
#recipe_response = recipe_chain.invoke({"food" : "bibimbap"})
#print(recipe_response)

final_chain = {"food": food_chain} | recipe_chain
final_response = final_chain.invoke({"country": "France"})
print(final_response)