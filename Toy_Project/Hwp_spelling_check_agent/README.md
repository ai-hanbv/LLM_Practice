### hwp 맞춤법 교정 llm

#### 목적
- 공무원 등 많은 국내 기업들은 hwp를 활용하고 있다. 하지만 온라인으로 이를 진행할 시 데이터의 외부 반출 우려가 생길 수 있기 때문에 사용을 꺼릴 수 있다. 하지만 로컬 llm을 활용하여 맞춤법을 
예시 : "p5. 결과가 나왓습니다. -> 결과가 나왔습니다." 와 같이 이런식으로 csv, 혹은 리스트 형태로 나열해준다면 문서 검토시 시간을 단축하는 결과가 있을거라 예상됩니다. 이러한 생각으로 이 프로젝트를 진행하게 되었습니다.

#### 기본 설정
IDE : cursor
Model : Gemma3
embedding : bge-m3
language : Python
Library : None
tunning env : Runpot or colab
venv : uv


#### 파인튜닝 기법
##### MultipleNegativesRankingLoss
##### 사용 데이터
- AIHub를 이용한 맞춤법 데이터 다운로드
