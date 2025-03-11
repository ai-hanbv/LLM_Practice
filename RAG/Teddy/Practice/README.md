#### MassagesPlaceHolder

```Python
from langchain_core.prompts import MessagesPlaceholder
```

이전메세지 및 새로 생성된 메세지들을 홀더에 머무르게 해준다.

### One, Few-shot
```Python
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts import FewShotChatMessagePromptTemplate
```

1. 예시를 제시해주고 추론을 시키는 프롬프트 방법이다. 1개일 경우 Oneshot이고, 2개 이상일 경우 Few-shot 이다. 쉽게 생각하면 LLM이 답을 쉽게 추론할 수 있게 가이드라인을 제시해주는 것이다.

### ExampleSelector

대표적으로 쓰는 이유가 2가지가 있다.
*  Fewshot의 경우 입력 토큰의 수가 많아지게 된다. 이런 상황에서 토큰 입력을 줄이기 위해 사용한다.
* LLM이 추론을 할 경우 출력해야 하는 양식이 다 다르다. 예를 들면 회의록 작성, 블로그 작성, 뉴스 작성 등 이런 상황에 맞춰서 비슷한 예제만 참고할 수 있게 해준다.

```Python
from langchain_core.example_selectors import MaxMarginalRelevanceExampleSelector, SemanticSimilarityExampleSelector
```
* 대표적으로 MaxMarginalRelevanceExampleSelector, SemanticSimilarityExampleSelector 방법이 있다.

1. MaxMarginalRelevanceExampleSelector
2. SemanticSimilarityExampleSelector

```Python
from langchain_core.example_selectors import BaseExampleSelector
```
* BaseExampleSelector 를 상속받아 custom ExampleSelector를 만들 수 있다. 


#### Langchain Hub

깃허브에 코드가 저장되어 있는 것처럼 프롬프트가 저장되어 있는 저장소가 있다.
```Python
from langchain import hub

# 프롬프트 가져오기
prompt = hub.pull("닉네임/프롬프트이름:hashcode")

# 프롬프트 등록하기
hub.push("닉네임/프롬프트이름", prompt)
```

- hashcode 는 commit 탭을 선택하면 버전이 있는데 그 칸에 넣어주면 된다. 넣어주지 않으면 최신 버전으로 선택된다.

### Output Parser
- LLM의 출력을 구조화된 출력으로 변경하여 사용자에게 전달해줄 수 있는 컴포넌트.

- LLM의 출력에는 메타 데이터, 본문, 토큰량 등등 여러가지의 데이터가 같이 포함되어 있는데 사용자의 입장에서는 답변창에 같이 표현할 시 가독성이 떨어진다. 이 외에 상황에도 사용하기 위함이다.

#### pydanticOutputParser
- 사용자 정의 구조화된 결과값을 받기 위한 모듈이다. pydantic 라이브러리를 활용하여 지침을 지정, 모델은 이 모듈을 참고하여 결과를 출력

- 프롬프트의 기존 예시를 제공하며 pydantic으로 생성한 클래스의 Field를 참고하여 프롬프트에 삽입해준다.

##### 주요 함수
1. get_format_instruction()
- 언어 모델이 출력해야할 정보의 지침
2. parse()
- 출력을 특정 구조로 변경