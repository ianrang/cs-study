#!/usr/bin/env sh
set -eu

SB=".sandbox"
mkdir -p "$SB/snippets" "$SB/requests"

cat > "$SB/snippets/sql-vulnerable.java" <<'DATA'
String query = "SELECT pw FROM member WHERE id='" + userInput + "'";
Statement st = conn.createStatement();
ResultSet rs = st.executeQuery(query);
DATA

cat > "$SB/snippets/sql-safe.java" <<'DATA'
PreparedStatement ps = conn.prepareStatement("SELECT pw FROM member WHERE id=?");
ps.setString(1, userInput);
ResultSet rs = ps.executeQuery();
DATA

cat > "$SB/requests/xss-request.txt" <<'DATA'
GET /search?q=<script>document.cookie</script> HTTP/1.1
Host: app.example
Cookie: SID=abc123
DATA

cat > "$SB/requests/csrf-form.html" <<'DATA'
<form action="https://bank.example/transfer" method="POST">
  <input name="to" value="attacker">
  <input name="amount" value="100000">
</form>
DATA

cat > "$SB/requests/crlf-request.txt" <<'DATA'
GET /redirect?next=/home%0d%0aSet-Cookie:%20admin=true HTTP/1.1
Host: app.example
DATA

cat > "$SB/requests/upload-note.txt" <<'DATA'
Filename: shell.php.jpg
Content-Type: image/jpeg
Body begins with: <?php system($_GET["cmd"]); ?>
DATA

cat > "$SB/observations.txt" <<'DATA'
Observations

1. `sql-vulnerable.java` builds SQL with string concatenation.
2. `sql-safe.java` uses parameter binding with PreparedStatement.
3. The XSS request includes script in user-controlled input.
4. The CSRF form lacks a per-request anti-CSRF token.
5. The CRLF request contains `%0d%0a`, which can split headers.
6. The upload sample uses double extension and misleading MIME type.
DATA

printf 'Created web vulnerability review fixtures in %s\n' "$SB"
