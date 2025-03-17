### MCP란?

**Model Context protocol**의 약자로 Antropic에서 개발한 표준형 통신 프로토콜이다.


#### Cluad Desktop - MCP

[참고링크](https://modelcontextprotocol.io/quickstart/user)

1. [Claud Desktop](https://claude.ai/download)에서 claud desktop을 다운받는다.
2. 설치 후 왼쪽 상단 메뉴에서 파일 -> 설정 -> 개발자 -> 시작하기 (단축키 : Ctrl + ,)를 누르면 창이 뜬다.
3. 편집하기를 눌러서 **claude_desktop_config.json** 을 눌러 아래 복붙한다.
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\username\\Desktop",
        "C:\\Users\\username\\Downloads"
      ]
    }
  }
}
```
4. username은 컴퓨터명으로 수정 후 해당 경로에 폴더가 위치하게 생성한다. 만약 다른 경로로 하고 싶다면 위 json 파일에 다른 경로를 입력하면 된다.
5. 저장 후 json 파일과 claud desktop을 종료한다.
6. cmd를 실행 후 node --version 명령어를 입력, Ex)v22.13.0 (다른 숫자가 나올 수 있음)이 뜨면 성공이다. 만약 node.js가 없으면 [node.js](https://nodejs.org/ko)에서 설치하면 된다.
7. 재실행 후 하얀 텍스트 박스 왼쪽 하단에 ![성공](./image/success.png)가 뜨면 성공이다.
8. uv python 설치 명령어
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
9. 설치 완료 후 프로젝트 만들고 싶은 폴더에 들어가서 아래 명령어를 순차적으로 실행한다. 세부 내용은 Result를 보면서 따라하면 된다.
```cmd
# 프로젝트 생성
uv init weather
# 가상환경 설치
uv venv
# 가상환경 활성화
.\.venv\Scripts\activate
# 의존성 설치
uv add mcp[cli] httpx
# 서버 파일 설치
new-itme weather.py
```

```Result
PS C:\DEV\Code\Python\RAG_Practice\MCP> uv init weather
Initialized project `weather` at `C:\DEV\Code\Python\RAG_Practice\MCP\weather`
PS C:\DEV\Code\Python\RAG_Practice\MCP> cd weather
PS C:\DEV\Code\Python\RAG_Practice\MCP\weather> uv venv
Using CPython 3.12.3 interpreter at: C:\DEV\Python\python.exe
Creating virtual environment at: .venv
Activate with: .venv\Scripts\activate
PS C:\DEV\Code\Python\RAG_Practice\MCP\weather> .\.venv\Scripts\activate
(weather) PS C:\DEV\Code\Python\RAG_Practice\MCP\weather> uv add mcp[cli] httpx
Resolved 27 packages in 627ms
Prepared 26 packages in 867ms
Installed 26 packages in 366ms
 + annotated-types==0.7.0                                                                                                                                   
 + anyio==4.9.0                                                                                                                                             
 + certifi==2025.1.31                                                                                                                                       
 + click==8.1.8                                                                                                                                             
 + colorama==0.4.6                                                                                                                                          
 + h11==0.14.0                                                                                                                                              
 + httpcore==1.0.7                                                                                                                                          
 + httpx==0.28.1                                                                                                                                            
 + httpx-sse==0.4.0                                                                                                                                         
 + idna==3.10                                                                                                                                               
 + markdown-it-py==3.0.0                                                                                                                                    
 + mcp==1.4.1                                                                                                                                               
 + mdurl==0.1.2                                                                                                                                             
 + pydantic==2.10.6
 + pydantic-core==2.27.2
 + pydantic-settings==2.8.1
 + pygments==2.19.1
 + python-dotenv==1.0.1
 + rich==13.9.4
 + shellingham==1.5.4
 + sniffio==1.3.1
 + sse-starlette==2.2.1
 + starlette==0.46.1
 + typer==0.15.2
 + typing-extensions==4.12.2
 + uvicorn==0.34.0
(weather) PS C:\DEV\Code\Python\RAG_Practice\MCP\weather> new-item weather.py


    디렉터리: C:\DEV\Code\Python\RAG_Practice\MCP\weather


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----      2025-03-17   오후 1:07              0 weather.py
```