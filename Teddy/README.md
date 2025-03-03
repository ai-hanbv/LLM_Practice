# Rag란?

### RAG (Retriever-Argumented-Generation)


### 기본적인 LLM

Query Input -> Prompt -> LLM (GPT, llama, ....) -> Output
- 이러한 흐름으로 초기에는 사용했으나 정보가 최신화되지 못하고 할루시네이션 즉 환각 현상이 발생하게 된다. 이를 위한 프롬프트 엔지니어링, 파인튜닝 등 여러 방법이 나왔고 RAG라는 방법론이 등장하게 된다.

### Rag 필요성

1. 정확한 정보를 제공한다. 관련성 높은 정보를 검색하여 정확하고 유용한 답변을 생성해낸다. 이러한 작업으로 할루시네이션을 줄일 수 있다.
2. 최적화 및 응답시간 단축. 정보를 빠르게 검색함으로써 전체적인 시스템 응답 시간을 단축하며 필요한 정보만 추출해서 자원의 사용을 최적화한다.


### Rag 처리 과정

Query Input -> Retriever -> Prompt + Retriever output -> LLM -> Output

#### 1. Query Input
 - 사용자의 질문을 백터 형태로 변환, 임베딩 단계와 유사한 기술을 사용한다. 

#### 2. Retriever

##### 동작 과정

1. 1번에서 넘어온 백터 형태로 변환된 쿼리 즉 질문을 코사인, 유클리드, MMR 등의 수학적 방법을 사용하여 유사성을 구한다.
2. Retriever 구성시 파라미터 N의 갯수에 따라 유사성이 높은 문서를 N개 가져온다.
3. N개의 문서를 프롬프트 생성하는 단계로 넘겨준다.

##### Rag 준비과정
    1. Document Load (pdf, excel, csv, ....)
    - 관련된 문서를 가져온다.
    2. Text Split
    - chunk 라는 기본 단위로 나눠준다.
    3. Embedding
    - chunk를 다차원 백터로 변환시켜준다.
    4. DB (Vector DB)
    - 백터의 형태로 DB에 저장시킨다.

#### 3. Prompt + Retriever Output
    - Query를 Prompt에 추가하여 주고 백터 DB에서 가져온 chunks를 묶어 LLM으로 전달하여 준다.
#### 4. LLM
#### 5. Output

### RAG의 대표적인 기법 2가지

1. Sparse
2. Dence

#### 컨텍스트 윈도우 (Context Window)
- 3번 (Prompt + Retriever Output)에서 LLM으로 들어가는 총 입력의 길이를 **컨텍스트 윈도우** 라고 한다.

- Retriever는 왜 Tokenizer가 아닌 DocumentSplitter 와 같은 도구를 쓰는지?
    - llm의 입력은 한계가 있다. 또한 외부 api를 사용하는 것은 토큰의 수가 많아질수록 금액이 증가하게 된다. 그래서 문서 읽고 chunk 라는 단위로 나눈 후 백터스토어 , DB 등 저장 후 retriever 사용시 가장 유사한 내용을 찾아 질문이랑 같이 전달하는 것이다. 이러한 방식으로 입력 토큰을 절약할 수 있고 질문에서 사용할 수 있는 컨텍스트 길이도 증가할 것이다.