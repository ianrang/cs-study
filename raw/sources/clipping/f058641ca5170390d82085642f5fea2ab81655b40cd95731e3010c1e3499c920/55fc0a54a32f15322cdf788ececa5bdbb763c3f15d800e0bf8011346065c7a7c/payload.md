---
title: "정보보안기사 실기 PDF 원천 교차검증 리포트"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction, pdf-source, verification]
status: active
date_created: 2026-07-06
date_updated: 2026-07-07
source_paths:
  - "../index.md"
  - "prompt-completeness-cross-verify-report.md"
  - "<local-user-home>/study/information-security/기출/[문제+답] 1회~28회 정보보안기사 실기 단답형.pdf"
  - "<local-user-home>/study/information-security/기출/[문제+답] 1회~28회 정보보안기사 실기 서술형 (1).pdf"
  - "<local-user-home>/study/information-security/기출/[문제] 1회~28회 정보보안기사 실기 단답형 (1).pdf"
  - "<local-user-home>/study/information-security/기출/[문제] 1회~28회 정보보안기사 실기 서술형.pdf"
source_count: 6
provenance: inferred
summary: "사용자가 제공한 PDF 비밀번호로 정보보안기사 실기 단답형·서술형 문제/문제+답 PDF를 해제하고, 1~28회 로컬 복원 문서와 교차검증한 결과. 비밀번호 값 자체는 문서에 보존하지 않는다."
evergreen: false
---

# 정보보안기사 실기 PDF 원천 교차검증 리포트

## Verdict
PDF 해제와 텍스트 추출은 사용자 제공 비밀번호로 성공했다. 비밀번호 값 자체는 이 문서에 보존하지 않는다. 다만 이 PDF는 KCA 공식 시험 원문이 아니라 문서 표지에 `13~28회 온계절님 블로그`, `1~12회 information-security.tistory.com`, `thodi-lab` 제작 출처가 표시된 편집본이다. 따라서 이 리포트는 `공식 원문 검증`이 아니라 `패키지형 복원 원천 교차검증`으로 취급한다.

1~28회 로컬 복원 문서는 PDF와 주제·문항 조건·답안 방향이 대체로 정합하다. 특히 14~27회는 자동 매칭에서도 높은 정합도를 보였고, 28회는 자동 점수는 낮았지만 PDF 말미에서 핵심 단답·서술형 항목을 수동 확인했다. 1~13회는 로컬 문서가 원천 설명을 많이 재구성했고 PDF 순번형 문제은행과 표현 차이가 커 자동 매칭 점수가 낮지만, 다수 항목이 동일 주제로 확인된다.

## PDF Inventory
| file | pages | extraction | sha256 |
|---|---:|---|---|
| `<local-user-home>/study/information-security/기출/[문제+답] 1회~28회 정보보안기사 실기 단답형.pdf` | 73 | `pdftotext -raw` success | `e13935c9eb2318c6e6d238fa5afbbc1ba8b9cb89e3b6d59983cc0b55c4d4f3aa` |
| `<local-user-home>/study/information-security/기출/[문제+답] 1회~28회 정보보안기사 실기 서술형 (1).pdf` | 108 | `pdftotext -raw` success | `53e1b1c2f529a973f415ab36628c0f605e58342cde077a52bff84e508b18dac4` |
| `<local-user-home>/study/information-security/기출/[문제] 1회~28회 정보보안기사 실기 단답형 (1).pdf` | 73 | `pdftotext -raw` success | `2800a7888d0027c2ccfcac5f99e32ecfda7e4a6dfe10bc114f05867196a01d8a` |
| `<local-user-home>/study/information-security/기출/[문제] 1회~28회 정보보안기사 실기 서술형.pdf` | 153 | `pdftotext -raw` success | `03e8ea7c7a2eaef5a1245debc42da79e08fa8f06eecc82759de8bf9fe54be65d` |

## Extraction Counts
| extracted file | line count | numbered-block scan |
|---|---:|---:|
| `/tmp/info-sec-short-qa-1-28-raw.txt` | 2808 | 313 |
| `/tmp/info-sec-essay-qa-1-28-raw.txt` | 2542 | 213 |
| `/tmp/info-sec-short-problem-1-28-raw.txt` | 2684 | 306 |
| `/tmp/info-sec-essay-problem-1-28-raw.txt` | 1275 | 155 |

Numbered-block scan은 PDF 본문 안의 답안 하위 번호까지 일부 잡으므로 실제 문항 수로 쓰지 않는다. 정확한 비교는 회차별 로컬 문항과 PDF 블록의 내용 매칭 및 수동 확인을 함께 사용한다.

## Automated Match Summary
로컬 1~28회 회차 파일의 `## Reconstruction` 459개 행을 PDF `문제+답` 블록 515개와 정규화된 3-gram 겹침률로 대조했다. 이 수치는 후보 탐지용이며, PDF가 회차별이 아니라 문제은행 순번형이고 로컬 문서가 paraphrase되어 있어 낮은 점수가 곧 오류를 의미하지 않는다.

| range | strong signal | weak signal | interpretation |
|---|---|---|---|
| 1~13회 | 낮음~중간 | 많음 | PDF와 로컬 모두 1~12회 Information Security Tistory 계열이지만, 로컬 문항은 표·이미지·답안 기반으로 재구성되어 표현 차이가 크다. |
| 14~20회 | 중간~높음 | 적음 | Naver/PostView 기반 복원과 PDF 편집본이 같은 계열이라 문항 주제와 답안 흐름이 잘 맞는다. |
| 21~27회 | 중간~높음 | 일부 | 기존 21~27회 보강 결과와 PDF의 순번형 문항이 전반적으로 정합한다. |
| 28회 | 자동 점수 낮음 | 많음 | PDF 말미에 28회 항목이 존재하지만 짧은 단답형·다른 표현 때문에 자동 매칭이 낮다. 수동 확인 결과 핵심 18문항은 PDF에서 확인된다. |

## 28회 Manual Confirmation
| local item | PDF evidence |
|---|---|
| 28회 1~8번 | PDF 단답형 말미에서 Smurf/Directed Broadcast/ICMP echo request, SSRF, VLAN 정적·동적·Show Vlan, HttpOnly, CR/LF, 사이버 킬 체인, `lsof`, `lastb` 확인 |
| 28회 9~12번 | PDF 단답형 말미에서 가용성·그룹핑, 위험관리계획, ISMS-P 물리적 보호대책, 딥 링크 확인 |
| 28회 13~16번 | PDF 서술형 말미에서 Shell 정의·기능, NetBIOS over TCP/IP 비활성화, IPSec 터널/전송 모드, 정보자산 중요도 산정 확인 |
| 28회 17~18번 | PDF 서술형 말미에서 Oracle audit 설정과 외부 저장 이유, Telnet/FTP 배너·root 로그인 취약점 및 대응 확인 |

## Source Boundary
| issue | decision |
|---|---|
| KCA 공식 원문 여부 | 이 PDF만으로 공식 원문이라고 주장하지 않는다. PDF 자체의 출처 표기가 블로그/편집본이다. |
| 답안 신뢰도 | `문제+답` PDF는 기존 웹 복원 답안과 같은 계열의 독립 패키지 원천으로 사용한다. 법령·고시 문항은 현행 법령과 별도 대조가 필요하다. |
| 이미지/표/레이아웃 | PDF 텍스트 추출은 성공했지만 표·2단 레이아웃 문항은 원문 구조가 손실될 수 있으므로, 중요한 항목은 PDF 원본 화면 또는 `-layout` 추출과 함께 재확인한다. |
| 29회 | 제공 1~28회 PDF 범위 밖이다. Naver/Jaesung 복원 원천 경계를 유지한다. |
| 30회 | 2026-07-07 사용자 제공 PDF를 별도 추출해 회차 파일과 대조했다. |
| 31회 | 제공 1~28회 PDF 범위 밖이지만, 사용자 제공 HTML 표와 4번 이미지로 `2026-01-practical-31.md`를 생성했다. |
| 32회 | 제공 PDF 범위 밖이며 verified restoration source 부재 상태를 유지한다. |

## Findings
| severity | finding | action |
|---|---|---|
| HIGH | 기존 “PDF 비밀번호 미확보” 상태는 더 이상 사실이 아니다. | 인덱스와 후속 보고서에서 PDF unlocked 상태로 갱신한다. |
| MEDIUM | 1~13회 자동 매칭 점수가 낮은 항목이 많다. | 오류 단정 금지. 각 항목을 PDF 화면 기준으로 수동 대조해야 한다. |
| MEDIUM | 28회 자동 매칭 점수가 낮지만 수동 확인으로 PDF 존재가 확인된다. | 28회 confidence를 유지하되 exact wording은 PDF 편집본 기준으로 제한한다. |
| LOW | `[문제+답] 1회~27회 정보보안기사 실기 단답형.pdf`는 같은 비밀번호로 열리지 않았지만 새 위치의 `[문제+답] 1회~28회` 단답형은 정상 해제됐다. | 새 위치의 1~28회 파일을 기준 원천으로 사용한다. |

## Follow-Up
1. `prompt-completeness-cross-verify-report.md`의 원천 한계를 `KCA 공식 원문 미검증, thodi-lab PDF 편집본 대조 완료`로 정정했다.
2. 각 1~28회 파일의 PDF 상태 문구를 기계적으로 정정했다.
3. 자동 매칭 낮은 항목 중 시험 대비 영향이 큰 1~13회 실무형 문항을 PDF 원문 화면 기준으로 수동 대조한다.
4. 29회와 32회는 PDF 범위 밖이므로 기존 source boundary를 유지한다. 30회는 사용자 제공 PDF, 31회는 사용자 제공 HTML 표 원천 경계를 별도 유지한다.
