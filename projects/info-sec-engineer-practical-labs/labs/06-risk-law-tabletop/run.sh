#!/usr/bin/env sh
set -eu

SB=".sandbox"
mkdir -p "$SB"

cat > "$SB/risk-register.csv" <<'DATA'
asset,cia,threat,vulnerability,likelihood,impact,current_control
ERP DB,H/H/H,unauthorized DB access,weak privileged account review,H,H,quarterly review only
Web server,M/M/H,web shell upload,extension-only upload validation,M,H,manual source review
HR spreadsheet,H/M/M,privacy leakage,broad shared folder permission,M,H,no periodic access review
DNS server,M/M/H,zone transfer leakage,allow-transfer any,L,H,none
DATA

cat > "$SB/privacy-flow.txt" <<'DATA'
Privacy Processing Flow

Collection:
- Name, phone, email, resident registration number
- Legal basis for resident registration number: user consent only

Storage:
- Resident registration number stored with MD5 hash
- Access logs retained for 3 months

Provision:
- Personal data transferred to partner over plaintext FTP

Destruction:
- Retention period: permanent
DATA

cat > "$SB/biometric-principles.txt" <<'DATA'
Biometric protection answer candidates:
- proportionality
- lawfulness
- purpose limitation
- transparency
- safety
- data subject control
DATA

cat > "$SB/observations.txt" <<'DATA'
Observations

1. ERP DB has high CIA value and weak privileged account review.
2. Web server upload validation is extension-only, which is weak.
3. HR spreadsheet has broad shared-folder permission and privacy risk.
4. DNS server has `allow-transfer any`, which can leak zone data.
5. Privacy flow has weak legal basis, weak hash choice, short log retention, plaintext transfer, and permanent retention.
DATA

cat > "$SB/answer-sheet.txt" <<'DATA'
Answer Sheet

Risk Register
For each row:
`asset -> threat/vulnerability -> risk -> response strategy -> control`

Privacy Flow
For each issue:
`processing stage -> issue -> required safeguard`

Biometric Information
Write six principles and one sentence for each.
DATA

printf 'Created risk/law tabletop fixtures in %s\n' "$SB"
