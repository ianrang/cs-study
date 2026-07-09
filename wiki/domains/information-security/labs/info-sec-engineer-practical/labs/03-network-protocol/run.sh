#!/usr/bin/env sh
set -eu

SB=".sandbox"
mkdir -p "$SB"

cat > "$SB/tcp-scan-summary.txt" <<'DATA'
A -> B TCP 25 SYN
B -> A TCP 25 SYN/ACK
A -> B TCP 25 RST
A -> B TCP 443 SYN
B -> A TCP 443 RST
A -> B TCP 110 SYN
no response
DATA

cat > "$SB/arp-table.txt" <<'DATA'
Gateway expected: 175.113.81.1 -> a1-b1-c1-d1-e1-f1
175.113.81.65 -> 90-9f-5e-00-2f-16
175.113.81.1  -> 90-9f-5e-00-2f-16
175.113.81.55 -> f4-e1-5e-7f-f0-8f
DATA

cat > "$SB/iptables-rules.txt" <<'DATA'
iptables -A OUTPUT -p icmp --icmp-type 8 -j DROP
iptables -A INPUT -p tcp --dport 23 -j DROP
iptables -A INPUT -p udp --dport 53 -s 192.0.2.10 -j ACCEPT
DATA

cat > "$SB/dns-amplification-note.txt" <<'DATA'
Repeated DNS ANY queries are sent from changing source ports.
The victim IP appears as the spoofed source.
Large DNS responses are reflected from open resolvers.
DATA

cat > "$SB/observations.txt" <<'DATA'
Observations

1. TCP 25 is open in the scan summary because SYN/ACK is returned.
2. TCP 443 is closed because RST is returned.
3. TCP 110 is filtered or blocked because no response is observed.
4. The ARP table maps the gateway IP to an unexpected MAC also used by another host.
5. The first iptables rule blocks outbound ICMP echo request type 8.
6. DNS amplification uses spoofed source IP and large reflected responses.
DATA

printf 'Created network protocol fixtures in %s\n' "$SB"
