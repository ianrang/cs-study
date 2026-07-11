#!/usr/bin/env sh
set -eu

SB=".sandbox"
mkdir -p "$SB/etc" "$SB/var/log" "$SB/files" "$SB/proc"

cat > "$SB/etc/passwd" <<'DATA'
root:x:0:0:root:/root:/bin/bash
alice:x:1001:1001:Alice:/home/alice:/bin/bash
svcweb:x:1500:1500:Service Web:/srv/web:/usr/sbin/nologin
DATA

cat > "$SB/etc/shadow" <<'DATA'
root:$6$rounds=5000$abc$HASHED:19800:0:99999:7:::
alice:$5$salt$HASHED:19800:0:90:7:::
svcweb:!:19800:0:99999:7:::
DATA

cat > "$SB/var/log/auth.log" <<'DATA'
Jul 09 09:01:10 lab sshd[120]: Failed password for invalid user admin from 10.0.0.55 port 51422 ssh2
Jul 09 09:02:11 lab sshd[121]: Failed password for alice from 10.0.0.55 port 51423 ssh2
Jul 09 09:03:14 lab sshd[122]: Accepted password for alice from 10.0.0.12 port 60100 ssh2
DATA

cat > "$SB/var/log/commands.log" <<'DATA'
alice pts/0 2026-07-09 09:04 /usr/bin/id
alice pts/0 2026-07-09 09:05 /usr/bin/find / -perm -4000
root  pts/1 2026-07-09 09:07 /usr/bin/chmod 4755 /tmp/demo-suid
DATA

touch "$SB/files/normal.txt"
touch "$SB/files/demo-suid"
touch "$SB/files/demo-sgid"
mkdir -p "$SB/files/shared-tmp"
chmod 0644 "$SB/files/normal.txt"
chmod 0755 "$SB/files/demo-suid"
chmod 0755 "$SB/files/demo-sgid"
chmod 0755 "$SB/files/shared-tmp"

cat > "$SB/files/permission-listing.txt" <<'DATA'
-rwsr-xr-x root root /usr/bin/passwd
-rwxr-sr-x root mail /usr/bin/mail
drwxrwxrwt root root /tmp
-rw-rw-rw- alice users /srv/share/open.txt
DATA

cat > "$SB/observations.txt" <<'DATA'
Observations

1. `/etc/passwd` uses `x` in the password field when password hashes are stored in `/etc/shadow`.
2. `$6$` indicates SHA-512 and `$5$` indicates SHA-256 in common shadow hash identifiers.
3. The sample auth log has repeated failed SSH logins from `10.0.0.55`.
4. `files/permission-listing.txt` contains SUID, SGID, sticky bit, and world-writable examples for exam-style interpretation.
5. `commands.log` is a text fixture standing in for process accounting / `lastcomm` style evidence.
DATA

cat > "$SB/answer-sheet.txt" <<'DATA'
Answer Sheet

Use this format:

`evidence -> security meaning -> recommended action`

## Q1

## Q2

## Q3

## Q4
DATA

printf 'Created %s\n' "$SB"
printf 'Read questions.md and compare with .sandbox/observations.txt\n'
