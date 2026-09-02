# 정보보안기사 실기 독립 실습 세트

이 영역은 기출문제 복원·분석 데이터셋과 분리된 실행형 학습 공간이다.

## 실행
```bash
cd projects/info-sec-engineer-practical-labs
./bin/run-lab.sh all
```

특정 Lab만 실행:

```bash
./bin/run-lab.sh 01-linux-hardening
```

정리:

```bash
./bin/clean-lab.sh all
```

## Lab 목록
| Lab | 학습 묶음 | 목적 |
|---|---|---|
| `01-linux-hardening` | Linux/Unix·Windows 계정·로그·권한 | 파일·로그·권한 샘플을 보고 실기 답안 작성 |
| `02-service-config` | 서비스 보안설정 | Apache/BIND/SMTP/xinetd 설정 취약점 해석 |
| `03-network-protocol` | 네트워크 프로토콜·장비·공격 | TCP/ICMP/DNS/iptables/ARP 증거 해석 |
| `04-web-vuln-review` | 웹 취약점·시큐어코딩 | SQLi/XSS/CSRF/SSRF/upload/CRLF 코드·요청 해석 |
| `05-ids-log-triage` | 관제·Snort·로그·침해사고 | Snort 룰, alert, 웹 로그, PCAP summary 해석 |
| `06-risk-law-tabletop` | 위험관리·접근통제·법규 | 위험평가표와 개인정보 보호조치 답안 작성 |

## 안전 원칙
- 기본 Lab은 Docker, 인터넷, 외부 서비스가 필요 없는 offline fixture 방식이다.
- 실행 산출물은 각 Lab의 `.sandbox/`에만 생성된다.
- 호스트 `/etc`, 사용자 계정, SSH, 방화벽, 브라우저 프로필, 실제 네트워크 대상은 변경하지 않는다.
- 공격 성공이 아니라 관찰 증거를 시험 답안으로 바꾸는 능력을 훈련한다.

## 학습 순서
1. `shared/answer-template.md`를 먼저 읽는다.
2. Lab `README.md`에서 기출 패턴과 금지 행동을 확인한다.
3. `run.sh`로 샘플을 생성한다.
4. `questions.md`에 답을 직접 쓴다.
5. `expected-observations.md`와 비교한다.
6. 부족한 부분은 기출 분석 문서나 공식 레퍼런스로 되돌아간다.
