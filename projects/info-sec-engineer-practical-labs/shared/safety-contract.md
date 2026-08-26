# 실습 안전 계약

## 허용
- Lab 내부 `.sandbox/`에 샘플 파일 생성
- 샘플 설정, 로그, 룰, HTTP 요청 텍스트 분석
- localhost 또는 offline fixture 기반 관찰

## 금지
- 인터넷 또는 제3자 시스템 대상 스캔·공격·부하 발생
- 호스트 `/etc`, SSH, 방화벽, 사용자 계정, 브라우저 프로필 변경
- 실제 flood, amplification, reverse shell, web shell, cracking 수행
- 실사용 서비스 코드에 취약 코드 주입

## 정리
각 Lab은 `.sandbox/` 외부 파일을 생성하지 않아야 한다. 정리 명령은 `.sandbox/`만 제거해야 한다.
