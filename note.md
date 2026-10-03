1.chat
- langchain_{} 유료모델은 api키 필요
    : `.env` 파일 만들어서 api키 관리
    - 공식문서 혹은 에러메시지 확잉

2.prompt
- llm.invoke(n)
- 허용 타입: string, PromptValue, list of BaseMessages
    - PromptValue
        ``` 
        from langchain_core.prompts import PromptTemplate

        prompt_template = PromptTemplate(
            template="what is the capital of {country}?",
            input_variables=["country"]
        )

        prompt = prompt_template.invoke({"country": "France"})
        ```
    - BaseMessage
        - 상속받은 대표 Message
        1) SystemMessge: LLM Application의 역할, 행동 방식, 규칙 등 지정
        2) HumanMessage: user 메시지
        3) AIMessage: 모델이 생성한 응답 (list에 질문+AIMessge로 넣으면 대화 이력처럼 인식하여 원하는 형식의 답변이 나오도록 유도)
        4) ToolMessage: Agent 만들 때 사용, tool 실행결과를 모델에 전달

3.output_parser
- type({응답}.content) 이 string  => StrOutputParser 많이 씀
- JsonOutputParser도 있지만 응답 형식이 일정하지 않아서 잘 쓰지 않음 => Pydantic 사용
```
from pydantic import BaseModel, Field

class Capital(BaseModel):
    capital: str = Field(description="The name of the capital")
    population: int = Field(description="The population of the capital")
    area: float = Field(description="The area of the capital")
    language: str = Field(description="The language of the capital")

response = llm.with_structured_output(Capital).invoke(prompt)

print(response.capital)  # => 요소 접근
print(response.population)
print(response.area)
print(response.language)

print(response.model_dump()) # => dic로 변환하여 출력(코드 내부 사용)
print(response.model_dump_json()) # => json으로 변환하여 출력(외부 전달 사용)

```


4.runnable (LCEL 사용)
- LCEL: LangChain의 구성 요소들을 |(파이프) 연산자로 연결해서 체인을 만드는 방법 ( 발전하면 => LangGraph)
- 공통 인터페이스면 묶기 가능
```
capital_chain = prompt_template | llm | output_parser

#parsed_response = output_parser.invoke(llm.invoke(prompt_template.invoke({"country": "France"})))
parsed_response = capital_chain.invoke({"country": "France"})
```
- chain도 runnable 이기 때문에 chain끼리 chain도 가능
 => 응답 내용을 넘겨서 다음 질문에 사용 가능
 ```
capital_chain = prompt_template | llm | output_parser
country_chain = country_prompt | llm | output_parser

#final_chain = {"country": country_chain} | capital_chain
#final_response = final_chain.invoke({"information" : "This country is very famous for its wine in Europs"})

final_chain = {"information" : RunnablePassthrough()} | {"country": country_chain} | capital_chain
final_response = final_chain.invoke({"This country is very famous for its wine in Europs"})
print(final_response)
 ```


 5. 프롬프트 중요성
- 비용: input <<<<<< output 
- 가장 간결하게 원하는 정보만 받을 수 있도록 프롬프트 작성해야함
- "어떤건 **하지말고** n에 대해 알려줘" 보다 "n에 대해 알려줘" -> pydantic으로 "n에 대한 내용이야?" 로 검증 -> 이후 로직 진행
- output에 대한 safety를 거는게 더 효율적

6. RAG
: 외부에서 관련 내용을 검색해서 프롬프트에 넣어주는 방식
- LLM은 학습된 내용만을 담고 있음 > 버전에서 가지고 있는 내용과 현실의 정보에 차이가 생김
    (BUT 학습을 많이 시킨다고 성능이 좋아지는 관계는 아님)
- 내부 문서등 알려지지 않은 내용은 LLM이 모름
- LLM을 학습시키지 않고 전달해준 내용을 기반으로 추론 및 답변하도록 만들 수 있음
