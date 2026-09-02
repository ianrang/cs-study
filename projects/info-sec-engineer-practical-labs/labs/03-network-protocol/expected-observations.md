# Expected Observations

| Question | Expected |
|---|---|
| Q1 | It is TCP half-open/SYN scan. 25 open, 443 closed, 110 filtered/no response. |
| Q2 | Yes. Gateway IP has a MAC different from the expected MAC and shared with another host. |
| Q3 | OUTPUT chain, ICMP protocol, echo request type 8, DROP action. |
| Q4 | Spoofed source causes reflected responses toward a victim; ANY can produce large responses. |
| Q5 | Mention source validation, directed broadcast disable, open resolver restriction, ACL/uRPF/rate limiting. |
