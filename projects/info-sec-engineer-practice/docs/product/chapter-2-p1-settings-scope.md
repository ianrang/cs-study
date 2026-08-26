# 2장 P1 설정형 학습 범위

## 1. 범위 결정

이 문서는 `wiki/domains/information-security/drafts/study/info-sec-engineer-network-security-study.md`에서 **P1**로 표시되고, 명령·룰·정책·구성 절차를 직접 다루는 항목을 학습 앱의 필수 설정형 범위로 정의한다. 완료는 제품별 모든 세부 명령을 암기한다는 뜻이 아니라, 원문이 제시한 통제 목적·적용 위치·결정적 구문·운영상 한계를 실기 답안 단위로 판독·작성할 수 있다는 뜻이다. 프로토콜 일반 원리, 공격 식별, 조회 전용 명령은 별도 학습 경로로 분리한다.

| 포함 기준 | 제외 기준 |
|---|---|
| 설정 명령, ACL·방화벽·Snort 룰, 접근·허용 정책, 보안 구성 선택, GUI 비활성화 절차 | 단순 개념 정의, 공격명 식별, 패킷·로그 조회 전용 명령, P2/P3 확장 설정 |

## 2. 학습 구조

```text
설정형 공통 판독
  → L2/네트워크 경계(ARP·VLAN·라우팅)
  → 반사·증폭 서비스(NTP)
  → 방화벽·ACL·iptables
  → 라우터 관리면·데이터면
  → 관리 서비스(SNMP·NetBIOS)
  → 탐지·보안정책(Snort·WAF/DLP/Anti-DDoS)
  → VPN 보안 구성(IPsec)
```

- 선행 관계는 개념의 필요성만 표현한다. 같은 주제의 문항은 용어 인식 → 설정 완성 → 상황 판정 → 서술형 자가 채점 순으로 연결한다.
- 각 자동 채점 문항은 원문에 명시된 명령·정책 또는 단일 판단 결과만 답으로 둔다. 여러 정상 답이 가능한 운영 설계는 서술형 자가 채점으로 둔다.
- `sourceRefs`는 원문 경로·행·확인 문구를 가져야 하며, P1 원문 밖의 제품별 세부 구문을 정답으로 강제하지 않는다.

## 3. P1 설정형 주제 목록

| 학습 주제 | 원문 근거 | 현재 상태 | 핵심 결과 |
|---|---:|---|---|
| 정적 ARP·ARP spoofing 보완 | 2.1.4 | 완료 | `arp -s`, 핵심 대상 제한, DHCP Snooping·DAI·Port Security 병행 |
| VLAN·스위치 하드닝 | 2.1.6 | 완료 | access 고정·DTP 비활성화·native VLAN 분리·trunk 최소화·Port Security |
| 라우팅 보안 정책 | 2.1.7 | 완료 | 인증·`passive-interface`·경로 필터링·관리 접근통제 |
| NTP 증폭 완화 | 2.2.3 | 완료 | `disable monitor`의 조건과 접근제어·rate limit·업그레이드 |
| 방화벽 정책 판독 | 2.3.1 | 완료 | Default Deny·shadow rule·최소 허용 |
| iptables 보강 | 2.3.2 | 완료 | 관리 SSH 허용·loopback·ESTABLISHED/RELATED·관리 접속 보존 검토 |
| ACL·uRPF | 2.3.3 | 완료 | Standard/Extended ACL·Ingress/Egress·Strict/Loose·대표 IOS 구문 |
| 라우터 관리면 | 2.3.4 | 완료 | 계정·secret·RSA·SSH·VTY ACL·timeout·AAA·시간·로그·백업 |
| 라우터 데이터면 | 2.3.4 | 완료 | Redirect·directed broadcast·unreachable·source route·Null0·외부 출발지 검증 |
| SNMP 관리 보안 | 2.3.5 | 완료 | v3 authPriv·community·RW·ACL·관리망 분리 |
| NetBIOS/SMB 노출 통제 | 2.3.6 | 완료 | 포트·Windows 비활성화·경계 차단 |
| IDS/IPS·Snort 룰·경보 정책 | 2.4.1~2 | 완료 | inline/TAP·header·options·threshold와 차단의 구분 |
| 보안 솔루션 정책 | 2.4.4 | 완료 | WAF/DLP/Anti-DDoS의 대상·예외·임계치·우회/스크러빙 |
| IPsec 보안 구성 | 2.5.1~2 | 완료 | AH/ESP/IKE/SA·전송/터널 모드의 보안 결과 |

### 3.1 완료 문항 단위

기존 문항만으로 세부 통제까지 완료되었다고 표시하지 않는다. 다음 16개는 2026-07-13 보강한 비중복 완료 단위이며, 기존 문항과 함께 위 표의 완료 상태를 뒷받침한다.

| 영역 | 추가 문항 ID | 자동/자가 채점 |
|---|---|---|
| ARP 병행 통제 | `arp-protection-03` | 자동 |
| VLAN 이중 태그·MAC flooding | `vlan-hardening-02`, `vlan-hardening-03` | 자동 |
| 라우팅 제어 평면 | `routing-security-02` | 자동 |
| 방화벽 정책 | `firewall-policy-review-02` | 자가 |
| iptables 운영 안전성 | `iptables-state-log-05` | 자가 |
| uRPF IOS 구문 | `urpf-04` | 자동 |
| 라우터 관리면 | `router-management-plane-02`, `router-management-plane-03` | 자동·자가 |
| SNMP 정책 | `snmp-management-security-02` | 자가 |
| NetBIOS GUI 설정 | `netbios-smb-control-02` | 자가 |
| Snort 옵션·경보 정책 | `snort-rule-policy-03`, `snort-rule-policy-04` | 자동·자가 |
| IDS/IPS 배치 | `ids-ips-placement-01` | 자동 |
| WAF·Anti-DDoS 정책 | `security-control-policy-02` | 자가 |
| IPsec 구성요소 | `ipsec-security-profile-02` | 자동 |

## 4. P2/P3 경계

NAT 세부 정책, TLS 하드닝, 무선 장비 하드닝, IPv6·DHCP·STP 설정은 원문 우선순위가 P2/P3이다. 이들은 P1 설정형 경로가 완료된 후 별도 확장 주제로 추가한다. P1 문항의 정답이나 선수관계에는 포함하지 않는다.

## 5. 검증 명제

| ID | 명제 | 검증 방법 |
|---|---|---|
| SCOPE-01 | P1 설정형 새 주제는 최소 한 개 이상의 실제 원문 `sourceRef`를 가진다. | builder source locator 검증 |
| SCOPE-02 | 활성 주제는 최소 한 문항을 가지며, 주제·문항 선수관계는 DAG다. | builder curriculum/prerequisite 검증 |
| SCOPE-03 | 자동 채점은 단일 명령·빈칸·판정만 사용한다. | stage handler와 answer contract 검증 |
| SCOPE-04 | 제품·버전 의존 세부 구문 또는 여러 정상 정책안은 서술형으로만 평가한다. | 콘텐츠 리뷰 |
| SCOPE-05 | P2/P3 항목은 P1 완료 조건을 오염시키지 않는다. | curriculum status 및 선수관계 검토 |
| SCOPE-06 | 실전 복합형은 여러 결정적 설정 빈칸만 자동 채점하고, 조건 의존·복수 정답 문제는 자동 채점하지 않는다. | stage handler와 콘텐츠 리뷰 |
| SCOPE-07 | 예상 문제는 기출 기반으로 표기하지 않으며, 예측 목록과 패턴 분석 근거를 모두 가진다. | builder provenance 검증 |

## 6. P1 기출·예상 문항 분류 근거

`기출 기반`은 실제 회차 데이터셋의 **복원된** 문항을 바탕으로 한 연습이라는 뜻이다. 현재 vault에는 공식 KCA 원문을 모두 보장하는 자료가 없으므로, 화면의 `source-derived` 상태를 함께 읽어야 한다. `예상 문제`는 다음의 두 근거가 동시에 있을 때만 등록한다.

| 분류 | P1 예시 | 직접 근거 | 검증 원칙 |
|---|---|---|---|
| 기출 기반·복원 | Smurf의 ACL + `ip directed-broadcast 100` 복합 설정 | 2022-02 복원 문제 15 | 명령·빈칸은 출처의 확인 문구와 일치해야 한다. |
| 기출 기반·복원 | ARP 캐시 조회 + 정적 ARP 대응 | 2024-01 복원 문제 17 | 원문 복원 답안이 조건 의존적이면 결정적 명령만 자동 채점한다. |
| 기출 기반·복원 | Snort `content` + `depth:14` 룰 완성 | 2018-01 복원 문제 15 | header와 option의 역할을 섞지 않는다. |
| 예상·분석 근거 | NTP monlist 반사 DDoS의 설정·ACL·업그레이드 | 예측 목록 15 + 서비스 보안설정 출제 패턴 | 기출처럼 표기하지 않고, 예측·분석 근거를 둘 다 보존한다. |

이 분류는 출제 가능성을 보장하지 않는다. 분석 문서가 말하는 반복은 동일 문구의 반복이 아니라 개념·실무기술의 반복이며, 복원 기출도 공식 문구 미검증 한계를 가진다. 따라서 앱은 “기출형 문장 암기”가 아니라 **명령/룰 판독 → 복합 빈칸 → 근거 확인** 순서를 유지한다.
