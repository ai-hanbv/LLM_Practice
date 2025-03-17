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
6. 재실행 후 하얀 텍스트 박스 왼쪽 하단에 ![성공](./image/success.png)가 뜨면 성공이다.
