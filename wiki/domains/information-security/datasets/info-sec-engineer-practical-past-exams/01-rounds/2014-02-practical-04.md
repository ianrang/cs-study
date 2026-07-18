---
title: "정보보안기사 실기 4회 2014년 2회 실기 복원"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction]
status: active
date_created: 2026-07-03
date_updated: 2026-07-06
source_paths:
  - "https://information-security.tistory.com/290"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 4회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 4회 2014년 2회 실기 복원

## Scope
- Exam mapping: 2014년 2회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | CVE 표기 `CVE-2014-6628`에서 (1) `2014`, (2) `6628`의 의미를 쓰시오. | (1) CVE ID가 예약되었거나 취약점이 공개된 연도 (2) 해당 연도에 부여된 취약점 고유 번호 | source-derived from Information Security Tistory; 2026-07-16 technical correction cross-checked against CVE Program identifier guidance |
| 2 | short | OWASP Top 10 취약점 설명의 명칭을 각각 쓰시오. (1) 신뢰할 수 없는 데이터가 명령어나 질의문의 일부로 인터프리터에 전달되어 예상치 못한 명령 실행이나 권한 없는 데이터 접근을 유발한다. (2) 신뢰할 수 없는 데이터를 검증 없이 웹 브라우저로 보내 공격자가 피해자 브라우저에서 스크립트를 실행하게 한다. (3) 로그온된 피해자의 세션 쿠키와 인증 정보를 자동 포함한 위조 HTTP 요청을 취약한 웹 애플리케이션에 강제로 보내도록 한다. | (1) Injection(인젝션) (2) XSS(Cross Site Script) (3) CSRF(Cross Site Request Forgery) | source-derived from Information Security Tistory; prompt descriptions restored |
| 3 | essay | 개인정보보호법 제17조에 따라 개인정보를 제3자에게 제공할 때 정보주체에게 알려야 하는 사항을 각각 쓰시오.<br>(1) 제공받는 자<br>(2) 제공받는 자의 이용 목적<br>(3) 제공 항목<br>(4) 보유·이용 기간<br>(5) 동의 거부권 및 불이익 | (1) 개인정보를 제공받는 자<br>(2) 개인정보를 제공받는 자의 개인정보 이용 목적<br>(3) 제공하는 개인정보의 항목<br>(4) 개인정보를 제공받는 자의 개인정보 보유 및 이용 기간<br>(5) 동의를 거부할 권리가 있다는 사실 및 동의 거부에 따른 불이익이 있는 경우 그 불이익의 내용 | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: five requested answer slots are explicit; statutory answer remains source-derived |
| 4 | essay | 위험 분석·평가 접근법의 빈칸을 채우시오. (A): 모든 시스템에 표준화된 보안대책 세트를 체크리스트로 제공한다. (B): 구조적 방법론보다 경험자의 지식으로 위험 분석을 수행한다. (C): 잘 정립된 모델에 기초해 자산·위협·취약성 분석 단계를 수행해 위험을 평가한다. (D): 위 세 방법을 혼합한다. | A : 베이스라인 접근법 B : 비정형화된 접근법 C : 상세 위험 분석 D : 복합 접근법 | source-derived from Information Security Tistory; prompt descriptions restored |
| 5 | short | 위험관리 용어의 빈칸을 채우시오. (A): 자산 위험을 수용 가능한 수준으로 유지하기 위해 위험을 분석하고 비용 대비 효과적인 보호대책을 마련하는 과정. (B): 정보자산에 영향을 줄 수 있는 위협·취약성·위험을 식별·분류하고 잠재 손실 영향을 분석하는 과정. (C): 위협과 취약성으로 인한 조직 피해를 평가하는 과정. (D): 위협에 대응해 자산을 보호하기 위한 물리적·기술적·관리적 대응책. | A : 위험관리 B : 위험분석 C : 위험평가 D : 위험대응 | source-derived from Information Security Tistory; prompt descriptions restored |
| 6 | short | 웹 서버를 대신해 브라우저 연결 요청에 응답하고, 클라이언트와 서버 사이에서 트래픽을 중계·수정할 수 있는 도구의 명칭을 쓰시오. 대표 도구로 Paros와 Burp Suite가 있다. | 프록시(Proxy) | source-derived from Information Security Tistory; answer block present |
| 7 | short | 다음 보안 용어의 명칭을 빈칸 (A), (B), (C)에 각각 쓰시오.<br>(A) 공격 시그니처 데이터베이스와 비교해 알려진 공격을 탐지하는 시스템<br>(B) 실제 공격을 정상으로 판단하는 오류<br>(C) 정상 트래픽을 공격으로 잘못 판단하는 오류 | (A) IDS(침입탐지 시스템)<br>(B) False Negative(미탐)<br>(C) False Positive(오탐) | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: three answer slots are explicitly mapped; exact official wording unavailable |
| 8 | short | 다음 5가지 스캔 방법 중 포트가 닫혀 있을 때만 응답이 오는 스캔 방식을 모두 고르시오. 보기: SYN Scan, FIN Scan, Xmas Scan, NULL Scan, Decoy Scan. | FIN Scan, Xmas Scan, NULL Scan | source-derived from Information Security Tistory; option list restored |
| 9 | essay | Telnet으로 웹 서버가 지원하는 HTTP 메소드를 확인하는 명령어를 작성하시오. 조건: 웹 서버 `hostname`, 포트 `80`, HTTP OPTIONS 메소드로 지원 메소드 목록 요청. | `telnet hostname 80`으로 연결한 뒤 `OPTIONS / HTTP/1.1`, `Host: hostname`, 빈 줄(CRLF 2회) 순으로 전송한다. | source-derived from Information Security Tistory; 2026-07-16 wording correction: HTTP request headers require a terminating empty line |
| 10 | essay | C 코드 `int main(int argc, char *argv[]) { char buff[8]; strcpy(buff, argv[1]); return 0; }`의 보안 취약점을 설명하고 안전한 코드로 수정하시오. | 취약점 : 8바이트 크기로 선언한 buff 변수에 strcpy()를 통해 입력값 크기 검증 없이 복사를 수행하므로 버퍼 오버플로우가 발생할 수 있다. 수정 방법 : strcpy() 대신 복사할 크기를 명시하는 strncpy() 또는 안전한 함수인 strcpy_s()를 사용하여 버퍼 크기를 초과하지 않도록 한다. strncpy(buff, argv[1], sizeof(buff) - 1); buff[sizeof(buff) - 1] = '\0'; | source-derived from Information Security Tistory; C code restored |
| 11 | essay | VPN 구성 프로토콜에 답하시오.<br>(A) 2계층(데이터링크 계층)에서 사용하는 VPN 프로토콜<br>(B) 3계층(네트워크 계층)에서 사용하는 VPN 프로토콜<br>(C) (B)의 두 가지 동작 모드와 각 모드의 연결 구간 및 보호 영역 | (A) PPTP, L2TP, L2F<br>(B) IPSec<br>(C) 전송 모드(Transport Mode) : End-to-End 방식으로 호스트 간 종단 통신에서 IP 페이로드(데이터)만 암호화하여 보호한다.<br>터널 모드(Tunnel Mode) : Gateway-to-Gateway 방식으로 라우터 간 통신에서 IP 헤더와 IP 페이로드 전체를 암호화하여 보호한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: A~C requirements restored from source text; exact official wording unavailable |
| 12 | essay | 웹 애플리케이션은 데이터베이스 오류나 조회 결과를 화면에 표시하지 않는다. 다음 접근 로그에서 `a` 조건의 응답 본문은 5,180바이트이고 `b` 조건의 응답 본문은 124바이트이다. `GET /member/login.php?user_id=1%27%20AND%20SUBSTR((SELECT%20password%20FROM%20member%20WHERE%20id=1),1,1)=%27a%27%20--%20&user_pw=x HTTP/1.1` / `GET /member/login.php?user_id=1%27%20AND%20SUBSTR((SELECT%20password%20FROM%20member%20WHERE%20id=1),1,1)=%27b%27%20--%20&user_pw=x HTTP/1.1` (1) 공격 기법의 명칭, (2) 그렇게 판단한 이유, (3) 이 요청을 반복하여 값을 추정하는 방법을 서술하시오. | (1) Boolean-based Blind SQL Injection 공격 (2) 오류나 조회 결과가 직접 표시되지 않지만, 사용자 입력에 SQL 조건식과 `SUBSTR()` 비교를 삽입하고 참·거짓에 따른 응답 본문 차이를 관찰하므로 Blind SQL Injection으로 판단한다. (3) id가 1인 사용자의 password 컬럼 값에 대해 `SUBSTR()`의 위치와 비교 문자를 한 글자씩 바꾸어 요청하고, 응답이 참일 때의 본문과 같은지 비교하여 각 문자를 순차적으로 추정한다. | source-derived from Information Security Tistory; 2026-07-18 prompt restoration: missing access-log evidence and three answer parts reconstructed from existing answer; Boolean response mechanism cross-checked against OWASP Blind SQL Injection guidance; exact official wording unavailable |
| 13 | essay | 개인정보보호법에 따른 개인정보 안전성 확보 조치 방안을 기술적·관리적·물리적 관점에서 각각 서술하시오.<br>(1) 내부 관리계획<br>(2) 접근 통제·권한 관리<br>(3) 암호화<br>(4) 접속 기록과 위·변조 방지<br>(5) 보안 프로그램<br>(6) 물리적 보관 조치 | (1) 개인정보의 안전한 처리를 위한 내부 관리계획의 수립·시행 → 관리적 관점<br>(2) 개인정보에 대한 접근 통제 및 접근 권한의 제한 조치 → 기술적·물리적 관점<br>(3) 개인정보를 안전하게 저장·전송할 수 있는 암호화 기술의 적용 → 기술적 관점<br>(4) 개인정보 침해사고 대응을 위한 접속 기록의 보관 및 위·변조 방지 조치 → 관리적·기술적 관점<br>(5) 개인정보에 대한 보안 프로그램의 설치 및 갱신 → 기술적 관점<br>(6) 개인정보의 안전한 보관을 위한 보관 시설의 마련 또는 잠금장치 설치 등 물리적 조치 → 물리적 관점 | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: six requested answer slots are explicit; statutory answer remains source-derived |
| 14 | essay | 다음은 내부 웹 서버 `192.0.2.10`의 HTTP 서비스(80번 포트)로 들어오는 요청에서 이미 검증된 PCRE 패턴 `evilstring`을 탐지하려는 Snort 룰이다. 이 문제에서는 PCRE 패턴 자체가 아니라 룰 헤더의 목적지 범위만 평가한다. `alert tcp any any -> any any (msg:"HTTP pattern"; pcre:"/evilstring/i"; sid:1000001; rev:1;)` (1) 목적지 주소와 포트를 `any any`로 설정한 문제점을 서술하시오. (2) 목적지 범위를 최소화한 수정 룰 헤더를 작성하시오. | (1) 목적지 주소와 포트가 모두 `any`이므로 모든 목적지 TCP 트래픽의 페이로드를 검사하게 되어 불필요한 검사 범위가 넓고 보안 장비 부하와 오탐 가능성이 증가한다. (2) `alert tcp any any -> 192.0.2.10 80 (...)` | source-derived from Information Security Tistory; 2026-07-18 prompt reconstruction: original malformed/incomplete PCRE snippet replaced with a self-contained rule-header scope question; only destination scoping is assessed; Snort rule header and PCRE syntax cross-checked against Snort documentation; exact official wording unavailable |
| 15 | essay | WPA 크래킹 과정에 답하시오. (1) `--bssid` 옵션에 입력하는 값의 의미, (2) `-c` 옵션의 의미, (3) `pw.lst` 파일의 용도, (4) 공격 대상 AP의 MAC 주소를 이용해 수행하는 공격의 목적을 서술하시오. | (1) 공격 대상 AP(무선 공유기)의 MAC 주소 (2) 공격 대상 AP에 연결된 클라이언트의 MAC 주소를 지정하는 옵션 (3) 사전(Dictionary) 공격을 위해 미리 정의된 패스워드 목록이 기록된 파일 (4) 공격 대상 AP의 MAC 주소를 이용하여 해당 AP와 클라이언트 간의 4-Way Handshake 패킷을 캡처하고, 사전 파일과 비교하여 WPA 패스워드를 크래킹하는 것이다. | source-derived from Information Security Tistory; option prompts restored |
| 16 | essay | 위험 분석 수치를 계산하시오. 회사 전체 자산 가치는 40억 원, 화재 발생 빈도는 5년에 1회, 화재 발생 시 손실 비율은 전체 자산의 30%, 소방 방재 시설 설치 비용은 수 천만 원, 화재 보험은 연 1억 원이고 화재 발생 시 10억 원을 보상한다. (1) AV, (2) EF, (3) SLE, (4) ARO, (5) ALE, (6) 위험 대응 대책 유형을 쓰시오. | (1) 자산 가치(AV) : 40억 원 (2) 노출 계수(EF) : 30%(0.3) (3) 단일 손실 예상액(SLE) : 40억 × 0.3 = 12억 원 (4) 연간 발생률(ARO) : 0.2 (5년에 1회 = 1/5) (5) 연간 예상 손실액(ALE) : 12억 × 0.2 = 2.4억 원 (6) 소방 방재 시설 설치 → 위험 감소(위험 완화) / 화재 보험 가입 → 위험 전가(위험 전이) | source-derived from Information Security Tistory; calculation conditions restored |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
