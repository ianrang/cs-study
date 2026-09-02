# java-review

## Knowledge pipeline validation

로컬 commit 전에 CI의 빠른 부분집합을 실행하려면 이 worktree에 tracked hook을 연결한다.

```bash
git config extensions.worktreeConfig true
git config --worktree core.hooksPath .githooks
```
