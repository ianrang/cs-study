# Expected Observations

| Question | Expected |
|---|---|
| Q1 | `x` means the password hash is stored separately in `/etc/shadow`. |
| Q2 | `$6$` is SHA-512 and `$5$` is SHA-256. |
| Q3 | `10.0.0.55` has repeated failed SSH attempts. It is suspicious and should be reviewed or blocked according to policy. |
| Q4 | SUID executes with file owner privilege, SGID with group privilege, sticky bit protects shared directories from arbitrary deletion, and world-writable files can be modified by any user. |
| Q5 | A good answer names the evidence, explains the risk, and gives a concrete check or mitigation. |
