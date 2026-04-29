# 2과목. 네트워크 보안

> 정보보안기사 필기 2과목. 출제기준 KCA 2023.1.1 ~ 2026.12.31, 20문제.
> OSI/TCP-IP 계층 구조부터 네트워크 공격 기법(DoS·DDoS·스캐닝·스푸핑·스니핑·원격접속), 보안 프로토콜(IPsec·SSL/TLS·VPN), 네트워크 보안 솔루션(방화벽·IDS/IPS·UTM·ESM 등) 까지 다룬다.

## 1. 출제기준 매핑

| 주요항목 | 세부항목 | 세세항목 | 작성 파일 |
|---|---|---|---|
| 1. 네트워크 일반 | 1) 네트워크 개념 이해 | OSI 7 Layers / TCP, UDP, IP, ICMP / Ethernet, LAN, Intranet, Extranet, Internet, CAN, PAN, HAN, SDN / IPv4·IPv6 Addressing, Subnetting, CIDR, VLSM, 데이터 캡슐화, Multicast, Broadcast / 공인주소·사설주소·정적·동적·NAT | 01·02 |
| | 2) 네트워크의 활용 | NIC, Router, Bridge, Switch, Hub, Repeater, Gateway, VLAN / Netbios, Netbeui, P2P / 유무선 네트워크 서비스 / ping, arp, rarp, traceroute, netstat, tcpdump 등 | 01·03 |
| 2. 네트워크 기반 공격기술의 이해 및 대응 | 1) 서비스 거부(DoS), 분산 서비스 거부(DDoS) 공격 | DoS/DDoS 유형별 동작원리·특징·대응 방법 | 05 |
| | 2) 스캐닝 | 포트 및 취약점 스캐닝의 동작원리·특징·대응 | 04 |
| | 3) 스푸핑 공격 | Spoofing 동작원리·특징·대응 | 04 |
| | 4) 스니핑 공격 | Sniffing, Session Hijacking 동작원리·특징·대응 | 04 |
| | 5) 원격접속 공격 | Trojan, Exploit 등 원격접속 공격 동작원리·특징·대응 | 06 |
| 3. 네트워크 보안 기술 | 1) 보안 프로토콜 이해 | 보안 프로토콜별 동작원리·특징, 응용 사례 | 07 |
| | 2) 네트워크 보안기술 및 응용 | Firewall, IDS, IPS, VPN, ESM, UTM, NAC, 역추적시스템 / Snort, 탐지툴, Pcap / 로그 분석 / 패킷 분석 / 역추적 / 악성코드 분석 도구 | 06·08 |

## 2. 파일 구성

| 파일 | 주제 | 출제기준 매핑 | 통합자료 매핑(line) | 2과목.txt 매핑(line) |
|---|---|---|---|---|
| `01.network-fundamentals.md` | OSI 7계층 / TCP-IP 4계층 / 네트워크 종류 / 네트워크 장비 / 네트워크 공유 | 1-1, 1-2 | 1394 ~ 1565 (네트워크 기본·장비) | 1 ~ 102, 124 ~ 127 |
| `02.network-protocols-and-addressing.md` | ARP/RARP/GARP / IP·ICMP / TCP·UDP / 단편화·MTU·MSS / 3·4-way Handshake / IPv4·IPv6 주소체계 / NAT | 1-1 (3·4), 1-2 | 1566 ~ 1747 (프로토콜) | 103 ~ 167, 173 ~ 269, 272 ~ 386 |
| `03.network-tools-and-wireless.md` | ping/traceroute/netstat/ifconfig/tcpdump/arp/whois 등 / 블루투스 / RFID / 무선랜(WEP·WPA·WPA2·EAP) / WAP·WTLS / 무선랜 크래킹 도구 / 무선랜 보안 메커니즘(인증·암호화·SSID 차단·MAC 주소 인증) | 1-2-3, 1-2-4 | 1748 ~ 2002 (관리·무선) + 2588 ~ 2609 (무선 크래킹) + 2933 ~ 3005 (무선랜 보안 메커니즘) | 387 ~ 437, 837 ~ 1022 |
| `04.scanning-sniffing-spoofing.md` | 풋프린팅·스캐닝·목록화 / nmap·TCP Connect/SYN/FIN/NULL/Xmas/ACK/UDP/Decoy / 스니핑(허브·스위치) / ARP·IP·ICMP 스푸핑·리다이렉트 / MITM / TCP 세션 하이재킹 | 2-2, 2-3, 2-4 | 2005 ~ 2268 (스니핑·세션·스캐닝) | 21 ~ 72, 147 ~ 172, 213 ~ 227, 250 ~ 271, 364 ~ 378, 438 ~ 551 |
| `05.dos-ddos-drdos.md` | DoS(Ping of Death·Land·Smurf·Teardrop·Bonk·Boink·Tiny Fragment·Fragment Overlap) / DDoS(Trinoo·TFN·Stacheldraht·TFN2K, UDP·ICMP·SYN Flood, HTTP GET, Hulk, Hash, CC, Slow 계열) / DRDoS(NTP·SSDP) / 봇넷·Fast Flux·DGA·Domain Shadowing / DNS 싱크홀 | 2-1 | 2270 ~ 2587 (DoS·DDoS·DRDoS) + 2629 ~ 2643 (DNS 싱크홀) | 552 ~ 836 |
| `06.remote-access-and-malware-tools.md` | 쉘 획득(바인드/리버스) / 익스플로잇 / 난독화·리버스 엔지니어링 / 악성코드 분류·정적/동적 분석·패킹 / 침해사고 종류(리버스 쉘 공격·루트킷 공격·DBD·APT) / APT 주요 침투 기법(스피어 피싱·워터링 홀·USB) / 사이버 킬 체인·MITRE ATT&CK / 공급망 공격 / 랜섬웨어 / 정보유출(은닉채널·방사) / Shell Shock 취약점 | 2-5, 3-2-6 | 5434 ~ 5773 (쉘·익스플로잇·난독화·악성코드·침해사고 종류·APT·사이버 킬 체인·MITRE ATT&CK) + 5775 ~ 5839 (공급망·랜섬웨어·정보유출) + 5862 ~ 5891 (Shell Shock) | 1과목 06 단원과 cross-ref (네트워크 관점) |
| `07.security-protocols.md` | VPN(PPTP·L2F·L2TP·IPsec·MPLS) / IPsec(AH·ESP·IKE·SA·SP·전송·터널 모드) / SSL/TLS(버전·Handshake·Record·완전·단축협상·PFS) / SSH 포트 포워딩(로컬·리모트) / SSL/TLS 취약점(Heartbleed·FREAK·LogJam·POODLE·DROWN) / S/MIME·PGP·PEM 보안 프로토콜 측면 | 3-1 | 2646 ~ 2839 (VPN·IPsec·SSL/TLS) + 5841 ~ 5861 (SSH 포트 포워딩) + 5892 ~ 5947 (SSL/TLS 취약점) | 1023 ~ 1224 |
| `08.security-solutions-and-monitoring.md` | VLAN·DMZ / 라우터 보안(ACL·Filtering·입출력 IP·주소 위변조 방지·BlackHole) / 클라우드 보안(SecaaS) / Snort 룰 / iptables(체인·룰·타겟·상태추적·확장 모듈) / 방화벽(NW·세션·응용, 스크리닝 라우터·듀얼홈드·스크린드 호스트·서브넷, NAT) / IDS·IPS(오용/이상, H-IDS/N-IDS, 인라인/미러링) / UTM·ESM·SIEM·SOAR·NAC·WIPS·EDR·DLP·DRM·SSO·EAM·IAM·HSM / 허니팟·허니넷 / DDoS 차단·SSL 오프로드·APT 대응·네트워크 포렌식 / PMS·EMM·MDM·MAM·MCM·BYOD·CYOD / 보안장비 운영 / 취약점 점검(Nessus·Nikto)·무결성 점검(Tripwire)·루트킷 점검(chkrootkit·/proc·Strace·rpm -V·lsattr·chattr) / 패킷 분석·로그 분석·역추적 / CVE·CWE | 3-2-1 ~ 3-2-5 | 2612 ~ 2627 (VLAN) + 2841 ~ 2932 (라우터 보안) + 4549 ~ 4582 (SecaaS) + 4638 ~ 5432 (Snort·iptables·보안 솔루션·보안장비 운영·취약점/무결성/루트킷 점검·CVE·CWE) | 1225 ~ 1344 |

> 통합자료에서 어플리케이션(DHCP·DNS·SNMP·FTP·Mail) 파트(line 3007 ~ 4503) 는 출제기준 3과목(어플리케이션 보안) 영역으로 분리되어 3과목 README에서 다룬다.
> 통합자료의 "어플리케이션 응용" 영역 중 클라우드 컴퓨팅(line 4505 ~ 4548), 블록체인(line 4584 ~ 4622), 사물 인터넷(line 4624 ~ 4636) 은 각각 1과목 1-1(Cloud / IoT) 또는 5과목(블록체인 운영) 영역으로 이관한다. 이 안에서 SecaaS(line 4549 ~ 4582) 만 보안 솔루션 카테고리로 2과목 08 에 포함한다.
> 1과목과 겹치는 영역(시스템 공격 기법·BoF·Race Condition·백도어 등) 은 1과목 06·07 단원에서 이미 다루었으므로, 2과목 06 단원에서는 네트워크 관점(원격 쉘 획득·DBD·APT 침투 단계·침해사고 분석 시나리오) 만 정리하고, 침해사고 분석 도구(chkrootkit·rpm -V·Tripwire·Nessus·Nikto) 는 08 단원으로 통합한다.

## 3. 학습 가이드

### 학습 순서 (권장)

1. **01 → 02 → 03** (기초): OSI/TCP-IP → 프로토콜 → 도구·무선 — 계층 구조와 패킷·주소 흐름을 먼저 잡는다.
2. **04 → 05** (수동·트래픽 공격): 스캐닝/스니핑/스푸핑 → DoS/DDoS — 패킷 단위 공격을 연속 학습.
3. **06** (능동·은닉 공격): 원격접속·악성코드·APT — 1과목 06·07 단원과 교차 학습.
4. **07** (방어 1 — 프로토콜): IPsec·SSL/TLS·VPN — 2·3과목 (특히 3과목 전자상거래 보안) 의 기반.
5. **08** (방어 2 — 솔루션·모니터링): 방화벽·IDS/IPS·SIEM·iptables·Snort — 침해 대응 흐름의 종착점.

### 우선순위 (출제 빈도 기준)

- 🔴 최상: 04(스캐닝·스니핑·스푸핑), 05(DoS·DDoS·DRDoS), 07(IPsec·SSL/TLS), 08(방화벽·IDS/IPS·Snort·iptables) — 분량·기출 비중 모두 높음
- 🟠 상: 01(계층·장비), 02(프로토콜·주소체계), 03(무선랜·도구)
- 🟡 중: 06(원격접속·악성코드 분석 도구) — 1과목과 겹치는 영역 있음

### 외부 보강 필요 영역 (통합자료에 없음 / 빈약)

이 영역은 작성 시 [외부자료 검증 체크리스트](../docs/외부자료-검증체크리스트.md) §2 의 출처를 1차 사용한다.

| 파일 | 보강 범위 | 1차 출처 |
|---|---|---|
| 02 | IPv4 헤더 필드 정의 / IPv6 헤더 / TCP 헤더 / UDP 헤더 / NAT(SNAT·DNAT·PAT) | RFC 791 (IPv4), RFC 8200 (IPv6), RFC 793 (TCP), RFC 768 (UDP), RFC 3022 (NAT) |
| 03 | 무선랜 인증 모델(EAP-TLS·EAP-TTLS·PEAP) / WPA3 / 802.11 표준 | IEEE 802.11 / 802.1X, KISA 무선랜 보안 가이드 |
| 04 | nmap 스캔 동작 표 / 스니핑 탐지(Promisc Detect) | Nmap Reference Guide, NIST SP 800-115 |
| 05 | DDoS 분류(대역폭 소진 vs 자원 소진), KISA 사이버대피소, 봇넷 사례 | KISA 침해사고 분석 보고서, NIST SP 800-61 |
| 06 | APT 공격 단계(Cyber Kill Chain), MITRE ATT&CK 전술/기법, 사이버 위협 인텔리전스 | Lockheed Martin Cyber Kill Chain, MITRE ATT&CK, KISA 침해사고 분석 보고서 |
| 07 | TLS 1.3 (RFC 8446) Handshake / IKEv2 (RFC 7296) / IPsec ESP (RFC 4303) | RFC 8446, RFC 7296, RFC 4301~4309, KCMVP |
| 08 | Snort 룰 문법 / iptables 체인 / IDS·IPS 표준 정의 / SIEM 표준 | Snort User's Manual, NIST SP 800-94 (IDS/IPS), netfilter.org iptables docs, OWASP |

## 4. 작성 원칙 (2과목 적용)

[외부자료 검증 체크리스트](../docs/외부자료-검증체크리스트.md) §3 을 따른다. 2과목 추가 사항:

1. **누락 금지**: 위 매핑표의 통합자료·2과목.txt 라인 범위를 반드시 빠짐없이 흡수한다.
2. **추론 금지**: 양쪽 원본에 없는 내용은 외부 자료 출처를 각주로 명시한 경우에만 추가한다. "아마/보통은/것으로 보인다/것으로 추정/자주 인용/자주 출제" 등 단정·추론 표현 금지.
3. **충돌 시 우선순위**: 출제기준 → 통합자료(체계적 표) → 2과목.txt(보충 사례)
4. **OCR 보정 명시**: 명백한 OCR 결함은 citation box(`> *원본 표기 보정*: ...`) 로 보정하며, 수치·플래그·식별자(예: 0x800, TTL 64, 502/udp 등) 는 보정하지 않는다.
5. **표·명령어·예시 보존**: 통합자료의 표 구조와 2과목.txt 의 명령 예시(예: `iptables -A INPUT -p tcp --syn`, `nmap -sS`, `tcpdump -i eth0`) 는 학습 가치가 높으므로 원본 표기 그대로 유지한다.
6. **서술 원칙**: 각 H2/H3 단위로 "정의 → 본문 → 표/예시 → 시험 포인트" 흐름을 따른다.
7. **외부 보강 출처 각주화**: 위 §3 외부 보강 영역은 모두 1차 출처(NIST·RFC·KISA·IEEE·MITRE 등) 를 각주로 명시한다. 위키피디아·민간 학원 자료는 1차 출처로 사용하지 않는다.
8. **1과목 cross-ref**: 1과목 06·07 단원과 겹치는 영역(APT·백도어·BoF·시스템 자원 고갈 등) 은 본문에서 cross-ref 로 연결한다 (예: `[1과목 06 §7. APT 공격과 MITRE ATT&CK](../01.system-security/06.system-attacks.md)`). 정확한 GFM 앵커는 cross-ref 작성 시 헤더 텍스트와 GFM slug 규칙에 맞춰 검증한다.

## 5. 참고 자료
- 출제기준 PDF: [`docs/info-sec-engineer-criteria-2023-2026.pdf`](../docs/info-sec-engineer-criteria-2023-2026.pdf)
- 외부자료 검증 체크리스트: [`docs/외부자료-검증체크리스트.md`](../docs/외부자료-검증체크리스트.md)
- 원본 자료: [`src/2과목.txt`](../src/2과목.txt) (1 ~ 1344), [`src/정보보안기사 정리_260214.txt`](../src/정보보안기사%20정리_260214.txt) (line 1394 ~ 3005 의 네트워크 챕터, line 4549 ~ 4582 의 SecaaS, line 4638 ~ 5947 의 침해사고 분석 및 대응 챕터. 어플리케이션 영역 line 3007 ~ 4503 은 3과목으로 이관, 어플리케이션 응용 안의 클라우드/블록체인/IoT 는 1·5과목으로 이관)
