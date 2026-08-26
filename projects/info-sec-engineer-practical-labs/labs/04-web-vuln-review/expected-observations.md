# Expected Observations

| Question | Expected |
|---|---|
| Q1 | SQL Injection risk from string concatenation; PreparedStatement parameter binding prevents input from changing query structure. |
| Q2 | The request alone proves reflected input risk only if server reflects it. Stored XSS needs evidence of persistence. |
| Q3 | CSRF token, SameSite cookie, Referer/Origin validation, re-authentication for sensitive actions. |
| Q4 | CR and LF can terminate a header line and inject another header or response content. |
| Q5 | Extension allowlist, MIME/content validation, random filename, non-executable storage, size limit, AV/scanning, authz check. |
