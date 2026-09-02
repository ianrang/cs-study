# Lab 01. Linux Hardening

## Objective
Linux/Unix 계정 파일, 로그, 권한, 명령어를 시험 답안 형태로 해석한다.

## Exam Pattern
- `/etc/passwd`, `/etc/shadow` 필드 의미
- `$1$`, `$5$`, `$6$` 해시 식별자
- `utmp`, `wtmp`, `btmp`, `lastlog`, `lastcomm`, `lsof`
- SUID, SGID, sticky bit, world-writable, umask

## Run
```bash
sh ./run.sh
```

Generated files stay under `.sandbox/`.

## Forbidden
- Do not read or modify host `/etc/passwd` or `/etc/shadow`.
- Do not create host users.
- Do not change host SSH, PAM, or shell profile settings.
