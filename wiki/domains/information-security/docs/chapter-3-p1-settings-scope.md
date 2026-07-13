# 3장 P1 서비스 보안설정 학습 범위

## 1. 범위 결정

이 문서는 `drafts/study/3장 정리.md`에서 P1으로 분류된 항목 중 **보안 속성·서버 설정·접근 정책·안전한 코드/데이터 흐름·감사와 검증 절차**를 앱의 설정형 학습 범위로 정의한다. 제품의 모든 세부 명령을 암기하는 범위가 아니라, 실기에서 반복되는 설정 빈칸·코드 판독·원리-대응 답안을 정확히 작성하는 범위다.

| 포함 | 제외 |
|---|---|
| HTTP/cookie/session, 웹 입력 방어, Apache/IIS/WAF, DNS/메일, DB 권한·감사, Secure SDLC 보완·재시험 | FTP 세부 설정, 모바일·클라우드·PKI, 제품/버전 종속 저빈도 옵션, 3.8 P3 참고 |

## 2. 문제 구조

```text
HTTP·쿠키·세션·인가
  → 입력·출력·서버 요청 방어
  → Apache·IIS·WAF
  → DNS·메일
  → DB 접근통제·감사
  → Secure SDLC·보완 이력
```

문제는 용어 인식 → 결정적 빈칸/설정 완성 → 상황 판정 → 복수 대응 서술형 자가 채점 순서로 구성한다. 자동 채점은 옵션명·명령·단일 판정처럼 답이 결정적인 경우만 사용한다. 제품 version, 배치 조건, 여러 정상 통제안이 가능한 답은 자가 채점한다.

## 3. P1 주제와 문항 수

| 앱 주제 | 문항 | 다루는 설정·정책 결과 |
|---|---:|---|
| `web-session-auth` | 6 | Secure/HttpOnly/SameSite, session ID 재발급, 객체별 서버 인가 |
| `web-input-defense` | 12 | PreparedStatement, XSS output encoding, CSRF token, SSRF, upload/path, XXE, CRLF, request smuggling |
| `web-server-hardening` | 12 | Apache `-Indexes`/TRACE/body/method/log, IIS/WAS 노출, WAF, 보안 header |
| `dns-mail-security` | 8 | BIND master/slave·`allow-transfer`·recursion, Sendmail access DB, SPF/DKIM/DMARC |
| `database-security-audit` | 5 | 최소권한, GRANT/REVOKE, listener 접근, Oracle 전통적 감사 |
| `secure-sdlc-review` | 5 | code/data 분리, 오류·비밀정보 log, 분석 산출물, SAST/DAST, retest 이력 |
| **합계** | **48** | 3장 P1 설정·정책 학습 단위 |

## 4. 기출 기반과 예상 문항

`기출 기반` 표기는 vault의 `01-rounds`에 보존된 **복원 문항**을 참조한다는 뜻이며, 공식 KCA 원문이 보장됐다는 뜻이 아니다. 화면의 `source-derived` 상태를 함께 확인한다. 48문항 중 SSRF 다계층 방어와 DNS zone transfer 답안은 반복 분석과 예측 목록을 모두 가진 `예상 문제`로 분리했다.

| 분류 | 근거 예 | 답안 원칙 |
|---|---|---|
| 기출 기반·복원 | HttpOnly, PreparedStatement, CR/LF, Apache Indexes/LimitRequestBody, Sendmail `makemap`, Oracle audit | 원문의 결정적 빈칸·구문만 자동 채점한다. |
| 예상·분석 근거 | SSRF 다계층 방어, DNS zone transfer 제한 | 기출처럼 표기하지 않고, 분석과 예측 근거를 동시에 보존한다. |

## 5. 검증 명제

| ID | 명제 | 검증 방법 |
|---|---|---|
| C3-01 | 여섯 활성 3장 주제는 각각 하나 이상의 문항을 가진다. | builder topic count 검증 |
| C3-02 | 각 문항은 실제 원문 또는 복원 기출의 path·line·excerpt를 가진다. | builder source locator 검증 |
| C3-03 | 자동 채점은 단일·결정적 답만, 복수 정상 답은 서술형만 사용한다. | stage/answer contract + 콘텐츠 리뷰 |
| C3-04 | 예상 문항은 패턴 분석과 예측 목록 근거를 모두 가진다. | builder provenance 검증 |
| C3-05 | 3장 선수관계는 단방향 DAG이며 UI 코드를 수정하지 않고 JSON만으로 노출된다. | builder prerequisite cycle 검증 |

## 6. 한계와 다음 범위

FTP, 모바일·BYOD, cloud/container, PKI 세부와 제품별 저빈도 syntax는 3장 P1 설정형 완료 조건에 넣지 않는다. 이들은 원문 P2/P3 우선순위에 따라 이후 별도 학습 팩으로 추가한다. 반대로 현재 48문항은 공격명 암기가 아니라 **근거 판독 → 코드/설정 통제 → 재시험·로그 검증**의 답안 구조를 반복하는 데 초점을 둔다.
