# Lab 02. Service Config

## Objective
Apache, BIND, SMTP, xinetd 설정 샘플에서 취약 설정과 보완 조치를 찾는다.

## Exam Pattern
- Apache `Options Indexes`, `TraceEnable`
- DNS zone transfer and `allow-transfer`
- SMTP relay restriction and access database
- xinetd `disable`, `only_from`, `no_access`, `instances`, `access_time`

## Run
```bash
sh ./run.sh
```

Generated files stay under `.sandbox/`.
