# 4과목. 정보보안 일반

> 정보보안기사 필기 4과목. 출제기준 KCA 2023.1.1 ~ 2026.12.31, 20문제.
> 정보보호의 핵심 보안요소 기술(인증·접근통제·키 분배·디지털서명) 과 그 토대가 되는 암호학(대칭키·공개키 알고리즘·해시함수·MAC) 의 이론과 표준을 다룬다.

## 1. 출제기준 매핑

| 주요항목 | 세부항목 | 세세항목 | 작성 파일 |
|---|---|---|---|
| 1. 보안요소 기술 | 1) 인증 | 사용자 인증 방식 및 원리 / 메시지에 대한 인증 방식 및 핵심 기술 / 디바이스에 대한 인증 기술의 원리 | 01 |
| | 2) 접근통제 | 접근통제 정책의 이해 및 구성 요소 / 접근통제 정책의 특징 및 적용 범위(임의적·강제적·역할 기반 등) / 접근통제 기법과 각 모델의 특징 | 02 |
| | 3) 키 분배 프로토콜 | 대칭 키 기반 분배 방식의 원리 및 운영 / 공개 키 기반 분배 방식의 원리 | 03 |
| | 4) 디지털서명 | 인증서 구조 및 주요 특징 / 디지털서명의 이해(종류·보안 요구 조건·특징·서명 방식 등) / PKI 구성방식 및 관리(계층구조·네트워크 구조·복합형 구조·CRL·OCSP 등) / 디지털서명 응용 원리 및 구조(은닉서명·이중서명 등) | 04 |
| 2. 암호학 | 1) 암호 알고리즘 | 암호 관련 용어 및 암호 시스템의 구성 / 암호 공격의 유형별 특징 / 대칭키 암호시스템 특징 및 활용(종류·구조·운영 모드·공격 기술 등) / 공개키 암호시스템의 특징 및 활용(종류·구조·특징) / 인수분해 기반 공개키 암호방식 / 이산로그 기반 공개키 암호방식 | 05 |
| | 2) 해시함수 | 해시함수의 개요 및 요구사항 / 해시함수별 특징 및 구조 / 메시지 인증 코드(MAC)의 원리 및 구조 | 06 |

## 2. 파일 구성

| 파일 | 주제 | 출제기준 매핑 | 통합자료 매핑(line) | 4과목.txt 매핑(line) |
|---|---|---|---|---|
| `01.authentication.md` | (1) 사용자 인증: 인증의 3요소(지식·소유·존재) + 다요소 인증(MFA) / (2) 패스워드 기반 인증·OTP(HOTP·TOTP·S/Key) / (3) 생체 인증(지문·홍채·얼굴·정맥·서명) + FAR·FRR·EER·CER / (4) 위치·행동 기반 인증 / (5) 통합 인증 — SSO / Kerberos v5 (AS·TGS·티켓) / SAML 2.0 / OAuth 2.0 / OpenID Connect 1.0 / FIDO2 (CTAP2 + WebAuthn) / (6) 메시지 인증 — MAC / HMAC / 디지털서명 비교 / (7) 디바이스 인증 — 시도-응답(Challenge-Response) / 상호 인증 / 802.1X·EAP / 디바이스 인증서(X.509) | 1.1 인증 | (없음) | (없음) |
| `02.access-control.md` | (1) 접근통제 개요·구성요소(주체·객체·접근권한·참조 모니터·TCB) / (2) 접근통제 정책 — DAC(임의적)·MAC(강제적)·RBAC(역할 기반)·ABAC(속성 기반) / (3) 접근통제 행렬·ACL·Capability List / (4) 접근통제 모델 — Bell-LaPadula(기밀성·NRU·NWD)·Biba(무결성·NRD·NWU)·Clark-Wilson(상업적 무결성·CDI·UDI·TP)·Brewer-Nash(이해충돌 회피·Chinese Wall)·Lattice 모델·Information Flow / (5) 보안 등급(BLP) — Top Secret·Secret·Confidential·Unclassified / (6) NIST RBAC 표준(Core·Hierarchical·Constrained) / (7) 책임 추적성·최소 권한·직무 분리 | 1.2 접근통제 | (없음) | (없음) |
| `03.key-distribution.md` | (1) 키 관리 개념·생명주기(생성·등록·저장·배포·갱신·폐기) / (2) 대칭키 분배 — KDC(Key Distribution Center) / Needham-Schroeder / Otway-Rees / Kerberos 키 분배 / (3) 공개키 분배 — Diffie-Hellman 키 합의 (DH·DHE·ECDH·ECDHE) / RSA 키 캡슐화(KEM)·OAEP / Station-to-Station 프로토콜 / (4) MITM 방어 — 인증된 DH / PKI 기반 / (5) 키 합의 vs 키 전송 / Forward Secrecy 개념 / (6) NIST SP 800-56A·56B·56C 키 합의·KDF / SP 800-57 키 관리 가이드라인 / (7) HSM(하드웨어 보안 모듈)·키 백업·키 에스크로 | 1.3 키 분배 프로토콜 | (없음) | (없음) |
| `04.digital-signature-pki.md` | (1) 디지털서명 개요·요구조건(위조 불가·인증·부인 방지·변경 불가·재사용 불가) / (2) 디지털서명 알고리즘 — RSA-PSS / DSA / ECDSA / EdDSA(Ed25519·Ed448) / (3) 인증서 구조 X.509 v3 — 필드(Issuer·Subject·SerialNumber·Validity·SubjectPublicKeyInfo)·확장(SAN·KeyUsage·ExtendedKeyUsage·BasicConstraints) / (4) PKI 구성요소 — CA·RA·VA·저장소·구독자 / (5) PKI 구조 — 계층 구조·네트워크(상호인증) 구조·복합형(브리지) 구조 / (6) 인증서 폐기 — CRL(Full·Delta) / OCSP(stapling 포함) / SCVP / (7) 응용 디지털서명 — 은닉 서명(Blind Signature)·이중 서명(Dual Signature, SET)·그룹 서명·다중 서명·위임 서명 / (8) 한국 PKI 운영 — 공인인증서 폐지·전자서명법(2020 전부개정)·인정 전자서명·KISA NPKI·GPKI | 1.4 디지털서명 + 3과목 08 cross-ref | (없음) | (없음) |
| `05.crypto-algorithms.md` | (1) 암호학 용어·구성요소(평문·암호문·키·암호화·복호화·Kerckhoffs 원칙) / (2) 암호 시스템 분류 — 대칭/비대칭·블록/스트림·고전(시저·비제네르)·현대 / (3) 암호 공격 분류 — Ciphertext-only·Known-plaintext·Chosen-plaintext·Chosen-ciphertext·Adaptive CCA / 부채널 공격(전력·타이밍·전자기) / 차분 공격·선형 공격 / (4) 대칭키 — DES/3DES(Feistel) / AES(SPN) / SEED / ARIA / LEA / HIGHT / RC4 / ChaCha20 / 블록 vs 스트림 / (5) 운영 모드 — ECB·CBC·CFB·OFB·CTR (NIST SP 800-38A) / 인증 암호 GCM·CCM (SP 800-38C·D) / XTS (SP 800-38E) / KW (SP 800-38F) / (6) 공개키 — RSA(인수분해) / Rabin / ElGamal(이산로그) / ECC(타원곡선 이산로그) / DH·ECDH(키 합의) / (7) 인수분해 기반 — RSA 키 생성·암복호화·서명 / RSA-OAEP·PKCS#1 v2.2 / (8) 이산로그 기반 — ElGamal·DSA·ECDSA / 타원곡선 표준(P-256·secp256k1·Curve25519·Curve448) | 2.1 암호 알고리즘 | (없음) | (없음) |
| `06.hash-and-mac.md` | (1) 해시함수 개요·요구사항(일방향성·약한 충돌 저항성·강한 충돌 저항성·계산 효율성·압축성) / (2) 해시함수 분류 — Merkle-Damgård(MD5·SHA-1·SHA-2) / Sponge(SHA-3·Keccak) / (3) 주요 해시함수 — MD5(취약·128bit) / SHA-1(취약·160bit) / SHA-2(SHA-224·256·384·512·512/224·512/256) / SHA-3(SHA3-224·256·384·512, SHAKE128·256) / LSH(국산) / HAS-160 / (4) 해시 공격 — 무차별 대입·생일 공격·랜덤 오라클 / 길이 연장 공격(Length Extension) / (5) MAC — HMAC(RFC 2104·FIPS 198-1) / CMAC(NIST SP 800-38B) / GMAC(SP 800-38D) / KMAC(SP 800-185) / Poly1305(RFC 8439) / (6) MAC vs 디지털서명 vs 해시 비교 / (7) 패스워드 해싱 — bcrypt·scrypt·Argon2·PBKDF2 (NIST SP 800-132·KDF) / Salt·Pepper·Stretching | 2.2 해시함수 | (없음) | (없음) |

> **통합자료·4과목.txt 매핑이 모든 단원에서 "없음" 인 이유**: 4과목 출제기준 (인증 원리·접근통제 모델·키 분배·PKI·암호 알고리즘 이론·해시함수) 의 핵심 영역은 통합자료(`정보보안기사 정리_260214.txt`) 와 `4과목.txt` 양쪽 모두에서 **다루지 않는다**. 통합자료에는 단편적인 키워드(SHA-256 ID 5, ECDHE TLS cipher suite, AES128, MD5 체크섬, 참조 모니터 등) 만 등장하며, 이는 모두 1·2·3 과목 작성 시 해당 단원에 흡수되었다. `4과목.txt` 는 파일명과 무관하게 snort/iptables / 보안 솔루션 / NTFS / APT / SSL/TLS 취약점(Heartbleed·POODLE·Logjam·DROWN) 등 사실상 1·2·5과목 영역만 포함한다. 따라서 4과목 학습자료는 **외부 1차 출처(NIST FIPS·SP / RFC / KISA / KCMVP / ISO/IEC / 국가법령정보센터 / 학술 표준) 100% 보강**으로 작성된다.
> 1·2·3 과목에 흡수된 4과목 관련 단편(Kerberos·DH·AES·SHA·CRL·MD5·DHE/ECDHE 등) 은 본 4과목 단원에서 표준 정의 기반으로 다시 정확히 정리하고, 1·2·3 과목 단원과 cross-ref 처리한다.
> 학습 흐름상 암호학(05·06) 이 보안요소 기술(01·02·03·04) 의 토대이지만, 본 README §3 학습 가이드는 출제기준 순서를 따르면서 의존성 흐름(05·06 → 03·04 → 01·02) 을 §0 들어가며에서 명시한다.
> 04 단원의 한국 PKI 운영(공인인증서 폐지·전자서명법·인정 전자서명) 은 5과목 (관리 및 법규) 영역과 cross-ref 가 발생한다. 4과목에서는 디지털서명 표준 정의 측면을 다루고, 5과목에서는 법령 측면을 다룬다.

## 3. 학습 가이드

### 학습 순서 (권장)

출제기준 순서는 1) 보안요소 기술 → 2) 암호학 이지만, **개념 의존성** 측면에서는 암호학이 보안요소 기술의 토대를 이룬다. 시험 대비 효율을 고려한 권장 순서는 다음과 같다:

1. **05 → 06** (암호학 토대): 대칭키·공개키 암호 알고리즘 + 운영모드 + 암호 공격 → 해시함수·MAC. 이후 단원의 모든 보안요소 기술이 이 토대 위에 구축된다.
2. **03 → 04** (키와 신원의 연결): 키 분배 프로토콜(05 의 공개키 알고리즘 활용) → 디지털서명·PKI(05 의 RSA·ECDSA + 06 의 해시 활용). PKI 의 인증서 구조는 디지털서명 + 해시 + 공개키 알고리즘의 종합이다.
3. **01 → 02** (사용자·시스템 측면): 인증(03·04 의 PKI·키 분배·디지털서명을 모두 응용) → 접근통제(인증 다음 단계). FIDO2·Kerberos 는 03·04 의 키 분배·PKI 와 직접 연결된다.

처음 학습하는 경우 출제기준 순서(01 → 06) 그대로 진행해도 무방하나, 05·06 을 먼저 한 번 훑은 후 01 부터 정독하는 것이 권장된다.

### 우선순위 (출제 빈도 기준)

- 🔴 최상: 05(대칭키·공개키·운영모드·공격), 06(해시·MAC), 04(디지털서명·PKI·CRL·OCSP·이중서명) — 4과목 기출의 절반 이상이 이 영역에서 출제된다.
- 🟠 상: 02(DAC/MAC/RBAC + BLP/Biba/Clark-Wilson/Brewer-Nash 모델), 01(Kerberos·OTP·생체인증·FIDO2·SSO)
- 🟡 중: 03(DH·ECDH·KDC·Needham-Schroeder)

### 외부 보강 출처 (모든 단원 — 통합자료 미보유)

본 4과목은 100% 외부 1차 출처 보강이며, [외부자료 검증 체크리스트](../docs/외부자료-검증체크리스트.md) §D 의 출처를 1차로 사용한다.

| 파일 | 보강 범위 | 1차 출처 |
|---|---|---|
| 01 | 사용자 인증 방식·원리 / 다요소 인증 / OTP·생체·SSO / Kerberos / SAML / OAuth / OIDC / FIDO2 / 메시지 인증(MAC) / 디바이스 인증(802.1X·EAP) | NIST SP 800-63-3·63A·63B·63C (Digital Identity Guidelines), RFC 4226 (HOTP), RFC 6238 (TOTP), RFC 4120 (Kerberos v5), RFC 4422 (SASL), W3C WebAuthn Level 2, FIDO2 CTAP2 (FIDO Alliance), OASIS SAML 2.0, RFC 6749 (OAuth 2.0), OpenID Connect Core 1.0, IEEE 802.1X-2020, RFC 3748 (EAP), ISO/IEC 19794 (생체인식 데이터 포맷) |
| 02 | 접근통제 정책·구성요소 / DAC·MAC·RBAC·ABAC / 접근통제 모델 (BLP·Biba·Clark-Wilson·Brewer-Nash·Lattice) / 보안 등급 / NIST RBAC 표준 | NIST SP 800-53 Rev. 5 (AC family), NIST SP 800-162 (ABAC), ANSI INCITS 359-2012 (RBAC), Bell & LaPadula 1976 (MTR-2997), Biba 1977 (MTR-3153), Clark & Wilson 1987 (IEEE S&P), Brewer & Nash 1989 (IEEE S&P), DoD 5200.28-STD (TCSEC, Orange Book), ISO/IEC 27001:2022 |
| 03 | 키 관리 생명주기 / KDC / Needham-Schroeder / Otway-Rees / Kerberos 키 분배 / Diffie-Hellman / ECDH / RSA-KEM / Forward Secrecy / Station-to-Station | NIST SP 800-56A Rev. 3 (DH·ECDH), NIST SP 800-56B Rev. 2 (RSA-OAEP·RSA-KEM), NIST SP 800-56C Rev. 2 (KDF), NIST SP 800-57 Part 1 Rev. 5 (Key Management), RFC 7296 (IKEv2), RFC 2631 (DH Key Agreement Method), Diffie & Hellman 1976 (IEEE Trans. Inf. Theory), Needham & Schroeder 1978 (CACM), Otway & Rees 1987, ISO/IEC 11770 (Key Management) |
| 04 | 디지털서명 표준·요구조건 / RSA-PSS·DSA·ECDSA·EdDSA / X.509 v3 인증서 / PKI 구조 / CRL·OCSP·SCVP / 은닉서명·이중서명·그룹서명 / 전자서명법 | FIPS 186-5 (Digital Signature Standard, 2023), RFC 5280 (X.509 PKI Certificate and CRL Profile), RFC 6960 (OCSP), RFC 5055 (SCVP), RFC 8410 (Ed25519/Ed448 in X.509), RFC 8017 (PKCS#1 v2.2 RSA), Chaum 1982 (Blind Signatures, Crypto '82), SET Specification Book 1·2·3 (1997), [전자서명법] (국가법령정보센터, 2020.6 전부개정·2020.12.10 시행), KISA 전자서명 인증서비스 가이드 |
| 05 | 암호학 용어·Kerckhoffs 원칙 / 암호 공격 유형 / DES·3DES·AES·SEED·ARIA·LEA·HIGHT·RC4·ChaCha20 / ECB·CBC·CFB·OFB·CTR·GCM·CCM·XTS·KW / RSA·Rabin·ElGamal·ECC·DH / 인수분해·이산로그·타원곡선 | FIPS 197 (AES, 2001), FIPS 46-3 (DES, Withdrawn 2005), NIST SP 800-67 Rev. 2 (3DES Deprecated 2023), NIST SP 800-38A·B·C·D·E·F·G (Block Cipher Modes), RFC 8439 (ChaCha20-Poly1305), TTAS.KO-12.0004 (SEED), KS X 1213-1 (ARIA), KS X 3246 (LEA), TTAS.KO-12.0040 (HIGHT), FIPS 186-5 (RSA·ECDSA·EdDSA), RFC 8017 (PKCS#1 v2.2), RFC 7748 (X25519·X448), SEC 2 (recommended elliptic curve domain parameters), KISA seed.kisa.or.kr (국산 암호 알고리즘), KCMVP 검증 모듈 목록 |
| 06 | 해시함수 요구사항 / Merkle-Damgård·Sponge / MD5·SHA-1·SHA-2·SHA-3·LSH·HAS-160 / 길이 연장 공격·생일 공격 / HMAC·CMAC·GMAC·KMAC·Poly1305 / 패스워드 해싱(bcrypt·scrypt·Argon2·PBKDF2) | FIPS 180-4 (Secure Hash Standard, SHA-1 Deprecated·SHA-2), FIPS 202 (SHA-3 Standard, Keccak), FIPS 198-1 (HMAC), RFC 2104 (HMAC), NIST SP 800-38B (CMAC), NIST SP 800-38D (GMAC), NIST SP 800-185 (cSHAKE·KMAC·TupleHash·ParallelHash), RFC 8439 (Poly1305), TTAS.KO-12.0276 (LSH), NIST SP 800-132 (Password-Based Key Derivation), RFC 7914 (scrypt), RFC 9106 (Argon2), Provos & Mazières 1999 (bcrypt) |

## 4. 작성 원칙 (4과목 적용)

[외부자료 검증 체크리스트](../docs/외부자료-검증체크리스트.md) §3 을 따른다. 4과목의 특수성을 반영한 추가 사항:

1. **외부 1차 출처 100%**: 본 4과목은 통합자료 매핑이 부재하므로 모든 사실 진술은 1차 출처 각주 [^N] 로 명시한다. 위키피디아·민간 학원 자료·블로그·요약 노트는 1차 출처로 사용하지 않는다.
2. **추론 금지**: "아마 / 보통은 / 것으로 보인다 / 것으로 추정 / 자주 인용 / 자주 출제" 등 단정·추론 표현 금지. 표준 본문에 명시되지 않은 영역은 "표준 정의" 가 아닌 "용어 사용 사례·운용 사례" 로 약화 표현한다.
3. **충돌 시 우선순위**: 출제기준 → 1차 출처(NIST·FIPS·RFC·KS·TTAS 등 표준 본문) → KISA/KCMVP 운영 가이드 → 학술 원논문(Bell-LaPadula·Biba·Clark-Wilson 등). 동일 사안에 대해 한국(KISA·KCMVP·전자서명법) 과 국제(NIST·RFC·ISO) 출처가 다를 경우 양쪽을 모두 명시하고 차이를 표기한다.
4. **표준 식별 정확성**: FIPS 표준 번호·발표 연도(예: FIPS 197 (2001), FIPS 180-4, FIPS 186-5 (2023), FIPS 202), RFC 섹션 번호(예: RFC 4120 §3.3 — Kerberos AS-REQ), NIST SP 부제목(예: SP 800-56A Rev. 3 — DH·ECDH 키 합의), KCMVP 인증 모듈명, 국산 암호 표준 식별자(TTAS.KO-12.0004·KS X 1213-1·KS X 3246) 는 작성 시점에 출처를 직접 확인하고 추측하지 않는다.
5. **표기 일관성**: SHA-256 (대시 포함, NIST 공식 표기), AES-128·AES-192·AES-256 (대시 포함), RSA-2048·RSA-3072·RSA-4096 (대시 포함), Ed25519·Ed448 (대시 없음), HMAC-SHA-256 (NIST 표기) 로 통일한다. 본 4과목 전체 단원에서 동일 알고리즘에 대해 표기 흔들림 금지.
6. **수치·라운드 수·키 길이 정확성**: DES 56bit·64bit 블록·16라운드 / 3DES 168bit / AES 128/192/256bit 키 - 10/12/14라운드·128bit 블록 / SEED 128bit 키·128bit 블록·16라운드 / ARIA 128/192/256bit 키 - 12/14/16라운드 / LEA 128/192/256bit 키 - 24/28/32라운드 등 표준에 명시된 수치는 정확히 인용한다.
7. **서술 원칙 (1·2·3 과목 정착)**: 각 H2/H3 단위로 "**정의(인용 박스) → 도입 단락(서술형) → 본문 → 표/예시 → 시험 포인트**" 흐름을 따른다. 표만으로 구성된 영역 금지 — 분류·체계·개념의 의미를 서술적으로 풀이하는 도입 단락 필수.
8. **cross-ref 정확성**: 1·2·3 과목 단원 및 4과목 단원 간 cross-ref 는 참조 대상 파일의 자체 §번호와 정확히 일치시킨다(H2 = `§N`, H3 = `§N-M`). 동일 파일 내부에서는 anchor 링크를 사용한다.
9. **한국 법령 시점 정확성**: [전자서명법] 인용 시 개정일과 시행일을 구분한다(2020.6.9 전부개정 → 2020.12.10 시행). KISA 가이드는 발표 연월·문서 명칭을 정확히 표기한다. KCMVP 인증 모듈은 인증서 번호와 인증 일자를 사용 시 명시한다.
10. **국제 표준 vs 국내 표준 분리**: AES (FIPS 197, NIST) 와 SEED·ARIA·LEA·HIGHT (KS·TTAS, KISA) 의 표준화 주체를 혼동하지 않는다. KCMVP 검증 알고리즘과 NIST FIPS 인증 알고리즘은 별개 인증 체계임을 본문에 명시한다.

## 5. 참고 자료

- 출제기준 PDF: [`docs/info-sec-engineer-criteria-2023-2026.pdf`](../docs/info-sec-engineer-criteria-2023-2026.pdf)
- 외부자료 검증 체크리스트: [`docs/외부자료-검증체크리스트.md`](../docs/외부자료-검증체크리스트.md) (특히 §D 4과목(암호학·인증) 보완)
- 원본 자료: 본 4과목은 통합자료(`src/정보보안기사 정리_260214.txt`) 와 `src/4과목.txt` 양쪽 모두에서 출제기준 핵심 영역(인증·접근통제·키 분배·디지털서명·암호 알고리즘·해시함수) 이 부재하다. 통합자료의 단편적 키워드는 1·2·3 과목 단원에 이미 흡수되어 있으며, 본 4과목은 그 단편들을 표준 정의 기준으로 다시 통합 정리하면서 cross-ref 한다.
- 1차 출처 빠른 접근:
  - [NIST CSRC](https://csrc.nist.gov/) — FIPS 표준 본문 + SP 800 시리즈 PDF
  - [IETF Datatracker](https://datatracker.ietf.org/) — RFC 본문
  - [KISA 암호이용 활성화](https://seed.kisa.or.kr/) — 국산 암호 알고리즘(SEED·ARIA·LEA·HIGHT·LSH) 표준 문서
  - [KCMVP 검증대상 암호모듈](https://seed.kisa.or.kr/kcmvp/) — KCMVP 인증 모듈 목록
  - [국가법령정보센터](https://www.law.go.kr/) — 전자서명법 등 국내 법령 현행본
