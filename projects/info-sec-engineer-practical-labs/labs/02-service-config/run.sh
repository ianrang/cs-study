#!/usr/bin/env sh
set -eu

SB=".sandbox"
mkdir -p "$SB/apache" "$SB/bind" "$SB/mail" "$SB/xinetd"

cat > "$SB/apache/httpd.conf" <<'DATA'
<Directory "/var/www/html">
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>
TraceEnable On
DATA

cat > "$SB/bind/named.conf" <<'DATA'
zone "example.test" IN {
    type master;
    file "example.test.zone";
    allow-transfer { any; };
};
options {
    recursion yes;
};
DATA

cat > "$SB/mail/access" <<'DATA'
localhost.localdomain RELAY
localhost RELAY
127.0.0.1 RELAY
spam.example REJECT
DATA

cat > "$SB/xinetd/echo" <<'DATA'
service echo
{
    disable = no
    socket_type = stream
    protocol = tcp
    wait = no
    user = root
    instances = UNLIMITED
    only_from =
}
DATA

cat > "$SB/observations.txt" <<'DATA'
Observations

1. Apache directory listing is enabled by `Options Indexes`.
2. Apache TRACE is enabled by `TraceEnable On`.
3. BIND zone transfer is open to `any`.
4. DNS recursion is enabled globally in the sample.
5. xinetd service is enabled and has unlimited instances with no source restriction.
6. SMTP access fixture allows relay only for localhost and rejects `spam.example`.
DATA

printf 'Created service configuration fixtures in %s\n' "$SB"
