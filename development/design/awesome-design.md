# 유명 서비스 디자인 시스템 레퍼런스 적용 가이드

## 1) 문서 목적

이 문서는 유명 서비스의 디자인 시스템 레퍼런스를 내 프로젝트에 빠르게 적용할 때 참고하는 기준 문서다.  
목표는 AI 에이전트가 `DESIGN.md`를 읽고 일관된 UI를 생성하도록 만드는 것이다.

## 2) 핵심 개념

- `DESIGN.md`는 Stitch 포맷 기반의 텍스트 디자인 문서다.
- `AGENTS.md`가 에이전트의 작업 규칙을 정의한다면, `DESIGN.md`는 시각적 외형과 톤을 정의한다.
- Figma, JSON 스키마, 별도 툴링 없이 마크다운 파일만으로 스타일 컨텍스트를 전달할 수 있다.

## 3) 제공 구성(3종 세트)

각 서비스 레퍼런스는 아래 3개 파일로 제공된다.

1. `DESIGN.md`: 디자인 원칙, 스타일 토큰, 컴포넌트 규칙 정의
2. `preview.html`: 라이트 모드 미리보기
3. `preview-dark.html`: 다크 모드 미리보기

## 4) DESIGN.md 표준 구조(9개 섹션)

모든 `DESIGN.md`는 아래 9개 섹션 구조를 따른다.

1. **Visual Theme & Atmosphere**: 무드, 밀도, 디자인 철학
2. **Color Palette & Roles**: 색상명, HEX, 기능적 역할
3. **Typography Rules**: 폰트 패밀리와 계층 규칙
4. **Component Stylings**: 버튼, 카드, 입력, 내비게이션, 상태 표현
5. **Layout Principles**: 간격 스케일, 그리드, 여백 원칙
6. **Depth & Elevation**: 그림자 시스템과 서피스 계층
7. **Do's and Don'ts**: 권장 패턴과 안티패턴
8. **Responsive Behavior**: 브레이크포인트, 터치 타깃, 축소 전략
9. **Agent Prompt Guide**: 빠른 색상 참조와 즉시 사용 가능한 프롬프트

## 5) 실무 적용 절차

1. 원하는 서비스의 `DESIGN.md`를 프로젝트 루트에 복사한다.
2. AI 에이전트에게 `DESIGN.md`를 기준으로 UI를 구현하도록 지시한다.
3. 필요 시 `preview.html`, `preview-dark.html`를 함께 확인해 스타일 일치 여부를 검증한다.

예시 지시:

`프로젝트 루트의 DESIGN.md를 기준으로 이 페이지를 구현해줘.`

## 6) 공식 접속처: getdesign.md

유명 서비스 스타일의 `DESIGN.md`를 내려받거나 탐색할 때 사용하는 공개 웹사이트다.

| 항목 | 내용 |
|------|------|
| **접속 URL** | [https://getdesign.md/](https://getdesign.md/) |
| **사이트 성격** | AI 코딩 에이전트용 `DESIGN.md` 컬렉션. 인기 웹·제품의 디자인 시스템을 참고해 프로젝트에 맞는 UI를 만들 때 쓰는 레퍼런스 허브다. |
| **공개 파일 수 (참고)** | 사이트 Quick Stats 기준 **70**개의 `DESIGN.md` 파일(2026-04-30 기준 스냅샷). |
| **탐색** | 카테고리 필터(예: AI & LLM, Developer Tools, Fintech 등), 검색·정렬, 개별 브랜드별 `DESIGN.md` 열람. |
| **부가 기능** | 계정 **Sign in**, **Request private DESIGN.md**(비공개 요청), 북마크·설치 수 등 메타 정보 표시. |
| **운영** | VoltAgent 팀이 유지한다(사이트 푸터 기준). |

직접 입력 시 주소는 스킴을 포함한 전체 문자열 **`https://getdesign.md/`** 로 연다.

## 7) 수록 컬렉션

사이트에 공개된 브랜드·서비스 기준으로 수십 개 이상의 디자인 시스템 레퍼런스가 있다(상세 목록·개수는 [getdesign.md](https://getdesign.md/)에서 확인).

- **AI & Machine Learning**: Claude, Cohere, ElevenLabs, Minimax, Mistral AI, Ollama, OpenCode AI, Replicate, RunwayML, Together AI, VoltAgent, xAI
- **Developer Tools & Platforms**: Cursor, Expo, Linear, Lovable, Mintlify, PostHog, Raycast, Resend, Sentry, Supabase, Superhuman, Vercel, Warp, Zapier
- **Infrastructure & Cloud**: ClickHouse, Composio, HashiCorp, MongoDB, Sanity, Stripe
- **Design & Productivity**: Airtable, Cal.com, Clay, Figma, Framer, Intercom, Miro, Notion, Pinterest, Webflow
- **Fintech & Crypto**: Coinbase, Kraken, Revolut, Wise
- **Enterprise & Consumer**: Airbnb, Apple, BMW, IBM, NVIDIA, SpaceX, Spotify, Uber

## 8) 라이선스 및 사용 시 주의사항

- 라이선스: MIT
- 레퍼런스는 복제 대상이 아니라 기준점이다.
- 제품 특성, 사용자 맥락, 접근성 요구사항에 맞게 조정해서 사용한다.
