#!/usr/bin/env sh
set -eu

SB=".sandbox"
mkdir -p "$SB"

cat > "$SB/snort.rules" <<'DATA'
alert tcp any any -> any 80 (msg:"HTTP GET Flooding Detect"; content:"GET / HTTP1."; nocase; depth:13; threshold:type threshold, track by_src, count 10, seconds 1; sid:1000999;)
alert tcp any any -> any 23 (msg:"Dangerous"; content:"anonymous"; depth:14; sid:1001000;)
DATA

cat > "$SB/alerts.log" <<'DATA'
[**] [1:1000999:0] HTTP GET Flooding Detect [**] 10.0.0.50:55221 -> 10.0.0.10:80
[**] [1:1001000:0] Dangerous [**] 10.0.0.51:44001 -> 10.0.0.20:23
DATA

cat > "$SB/access.log" <<'DATA'
10.0.0.50 - - [09/Jul/2026:10:00:01 +0900] "GET / HTTP1.1" 200 123 "-" "stress-client"
10.0.0.50 - - [09/Jul/2026:10:00:01 +0900] "GET / HTTP1.1" 200 123 "-" "stress-client"
10.0.0.60 - - [09/Jul/2026:10:02:00 +0900] "GET /login HTTP/1.1" 200 321 "-" "normal-browser"
DATA

cat > "$SB/observations.txt" <<'DATA'
Observations

1. The first rule targets HTTP GET flooding by content and rate threshold.
2. `nocase` makes content matching case-insensitive.
3. `depth:13` restricts matching to the first 13 bytes.
4. `threshold:type threshold, track by_src, count 10, seconds 1` tracks source IP rate.
5. The second rule detects `anonymous` within the first 14 bytes to telnet port 23.
6. Rules with `any any -> any any` can increase false positives and inspection cost.
DATA

printf 'Created IDS/log triage fixtures in %s\n' "$SB"
