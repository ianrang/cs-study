# Cursor / VS Code 코드 추천·자동완성 활성·비활성 가이드

## 1. Cursor AI (인라인 AI 제안)

Cursor는 **Cursor Tab**이라는 AI 기반 인라인 코드 제안 기능을 제공합니다.

### 방법 A: 설정 메뉴
- **Cursor Settings** 열기: `Ctrl+Shift+J`
- **Features** → **Cursor Tab** 이동
- **Enabled** / **Disabled** 선택

### 방법 B: 화면 하단 토글
- 에디터 **우측 하단**의 **Cursor Tab** 버튼 클릭으로 즉시 켜기/끄기

### 방법 C: 단축키 설정
1. `Ctrl+Shift+P` → "Open Keyboard Shortcuts" 검색
2. "Toggle Cursor Tab" 검색
3. 원하는 단축키 지정 (예: `Ctrl+Shift+Space`)

### 방법 D: settings.json
```json
"cursor.cpp.enabled": false   // Cursor Tab 비활성화
```

---

## 2. Visual Studio Code (IntelliSense / 일반 자동완성)

VS Code의 기본 자동완성은 IntelliSense와 Quick Suggestions로 동작합니다.

### 완전 비활성화
`Ctrl+,` → Settings → `settings.json` 열기 후:

```json
{
  "editor.quickSuggestions": {
    "other": false,
    "comments": false,
    "strings": false
  },
  "editor.suggestOnTriggerCharacters": false,
  "editor.wordBasedSuggestions": "off"
}
```

### 인라인 제안(회색 유령 텍스트)만 끄기
```json
"editor.inlineSuggest.enabled": false
```

### 파라미터 힌트만 끄기
```json
"editor.parameterHints.enabled": false
```

### 다시 활성화
- 위 설정을 `true`로 변경하거나 해당 항목을 삭제

### 수동 트리거
비활성화 후에도 `Ctrl+Space`로 필요할 때만 제안을 띄울 수 있습니다.

---

## 3. 설정 파일 위치 (Windows)

| 에디터 | 경로 |
|--------|------|
| Cursor | `%APPDATA%\Cursor\User\settings.json` |
| VS Code | `%APPDATA%\Code\User\settings.json` |

---

## 4. 요약

| 기능 | Cursor | VS Code |
|------|--------|---------|
| AI 인라인 제안 | Cursor Tab (Features) | - |
| 일반 자동완성 | IntelliSense | `editor.quickSuggestions` |
| 인라인 유령 텍스트 | Cursor Tab | `editor.inlineSuggest.enabled` |
| 빠른 토글 | 하단 Cursor Tab 버튼 | - |
