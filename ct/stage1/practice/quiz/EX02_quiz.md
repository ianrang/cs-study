Q1. Scanner가 느린 이유는?
=> 문제부터가 이상한 뭐에 비해서 Sacnner 느린 이유가 되어야 하는거 아닐까요?
Scanner는 기본적으로 OS 버퍼에서 바이트 단위로 하나씩 읽어 오는데, 매번 OS 버퍼 호출을 수행하기 때문이다.


Q2. `BufferedReader`의 `readLine()`은 무엇을 반환하는가?
 BufferedReader의 버퍼에 데이터가 있으면 한줄 단위로 읽고, 없으면 InputStreamReader에서 사용자 입력을 받아와서 읽는다.  

Q3. `nextInt()` 후 `nextLine()`을 호출하면 빈 문자열이 반환되는 이유는?
=> nextInt()에서 사용자가 입력하면 정수와 엔터(개행)까지 같이 입력이되는데, nextInt()에서 정수만 꺼내오고, 개행은 버퍼에 그대로 남아 있는데, 다음 nextLine()은 개행까지 읽는데 버퍼에 남아 있는 개행을 읽고 종료되기 때문이다.
여기서 말하는 버퍼는 OS 버퍼를 의미한다.

Q4. `StringTokenizer`의 기본 구분자는 무엇인가?
기본 구분자는 space이며, StringTokenizer의 생성자에서 두번째 인자로 구분자를 지정할 수 있다.

Q5. `BufferedWriter` 사용 후 반드시 호출해야 하는 메서드는?

flush() 또는 close()이다.
계속 버퍼를 사용할 거면 flush(), 버퍼 사용을 종료할 거면 clo
