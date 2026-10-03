from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3.5:2b")

response = llm.invoke("what is the capital of France?")

print(response.content)