# Expected Observations

| Question | Expected |
|---|---|
| Q1 | `Options Indexes` enables directory listing. Use `Options -Indexes` or remove `Indexes`. |
| Q2 | TRACE can expose request data and is usually disabled with `TraceEnable Off`. |
| Q3 | Zone transfer to `any` can expose internal DNS records. Restrict it to trusted secondary DNS IPs. |
| Q4 | `RELAY` permits mail relay for listed hosts. `REJECT` denies the listed domain or host. |
| Q5 | Disable unnecessary services, set `only_from`, `no_access`, finite `instances`, and access time limits. |
