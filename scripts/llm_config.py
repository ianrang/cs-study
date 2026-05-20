#!/usr/bin/env python3
"""
LLMResolver — _meta/llm-config.yaml 단일 진입점.

사용:
    from scripts.llm_config import LLMResolver
    resolver = LLMResolver()
    spec = resolver.resolve("ingest")          # ModelSpec
    chain = resolver.fallback_chain("ingest")  # List[ModelSpec]
    resolver.invalidate_cache()

CLI:
    python3 scripts/llm_config.py resolve ingest
    python3 scripts/llm_config.py invalidate
    python3 scripts/llm_config.py list

Bash wrapper: scripts/llm-resolve.sh
SKILL.md frontmatter wrapper: `model_profile: <alias>` → resolver 자동 호출

규약:
- model_id 직접 인용 금지 (lint.py 차단)
- profile alias 만 사용
- env override: KURNELL_LLM_PROFILE_<NAME>=<alias>
- cache TTL 30s
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML 필요. `pip install pyyaml`", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "_meta" / "llm-config.yaml"

# cost_tier 순서 (높음 → 낮음). fallback chain 검증 시 사용.
COST_TIER_ORDER = ["high", "medium", "low", "free"]


@dataclass
class ModelSpec:
    alias: str
    provider: str            # claude-code | ollama | openai | ...
    model_id: str
    context: int
    cost_tier: str
    fallback: Optional[str] = None
    fallback_max_tier: Optional[str] = None
    deprecated: bool = False
    endpoint: Optional[str] = None  # ollama 등 외부 endpoint

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class LLMResolver:
    config_path: Path = CONFIG_PATH
    _cache: dict[str, ModelSpec] = field(default_factory=dict)
    _cache_loaded_at: float = 0.0
    _cache_ttl_seconds: float = 30.0
    _config: dict = field(default_factory=dict)

    def _load(self) -> None:
        """YAML 파일 read + cache TTL 확인."""
        now = time.time()
        if self._cache and (now - self._cache_loaded_at) < self._cache_ttl_seconds:
            return
        if not self.config_path.exists():
            raise FileNotFoundError(f"llm-config.yaml 부재: {self.config_path}")
        with open(self.config_path, encoding="utf-8") as f:
            self._config = yaml.safe_load(f)
        self._cache_ttl_seconds = (
            self._config.get("resolver", {}).get("cache_ttl_seconds", 30.0)
        )
        self._cache = {}
        for alias, spec in self._config.get("models", {}).items():
            self._cache[alias] = ModelSpec(
                alias=alias,
                provider=spec["provider"],
                model_id=spec["model_id"],
                context=spec.get("context", 0),
                cost_tier=spec["cost_tier"],
                fallback=spec.get("fallback"),
                fallback_max_tier=spec.get("fallback_max_tier"),
                deprecated=spec.get("deprecated", False),
                endpoint=spec.get("endpoint"),
            )
        self._cache_loaded_at = now

    def _env_override(self, profile: str) -> Optional[str]:
        """KURNELL_LLM_PROFILE_<NAME> env 검사."""
        prefix = self._config.get("resolver", {}).get("env_override", "KURNELL_LLM_PROFILE_")
        env_var = f"{prefix}{profile.upper().replace('-', '_')}"
        return os.environ.get(env_var)

    def resolve(self, profile: str) -> ModelSpec:
        """Profile alias → ModelSpec. env override 우선."""
        self._load()
        override = self._env_override(profile)
        if override:
            if override not in self._cache:
                raise ValueError(f"env override alias '{override}' not in models")
            return self._cache[override]

        profiles = self._config.get("profiles", {})
        alias = profiles.get(profile)
        if not alias:
            # 미정의 profile → default
            alias = profiles.get("default")
        if not alias:
            raise ValueError(f"profile '{profile}' 미정의 + default 미정의")
        if alias not in self._cache:
            raise ValueError(f"profile '{profile}' → alias '{alias}' 가 models 미정의")
        spec = self._cache[alias]
        if spec.deprecated:
            print(f"WARN: alias '{alias}' deprecated. 교체 권장", file=sys.stderr)
        return spec

    def fallback_chain(self, profile: str) -> list[ModelSpec]:
        """resolve(profile) 시작으로 fallback 체인. cost_tier <= current 만 허용."""
        self._load()
        chain = []
        spec = self.resolve(profile)
        chain.append(spec)
        seen = {spec.alias}
        ceiling = spec.fallback_max_tier or spec.cost_tier
        ceiling_idx = COST_TIER_ORDER.index(ceiling)

        current_alias = spec.fallback
        while current_alias:
            if current_alias in seen:
                raise ValueError(f"fallback cycle 검출: {' → '.join(seen)} → {current_alias}")
            if current_alias not in self._cache:
                raise ValueError(f"fallback alias '{current_alias}' missing in models")
            next_spec = self._cache[current_alias]
            next_idx = COST_TIER_ORDER.index(next_spec.cost_tier)
            if next_idx < ceiling_idx:
                # cost_tier 가 ceiling 보다 높음 (more expensive) → reject
                raise ValueError(
                    f"fallback chain cost_tier 위반: '{next_spec.cost_tier}' > ceiling '{ceiling}'"
                )
            chain.append(next_spec)
            seen.add(current_alias)
            current_alias = next_spec.fallback
        return chain

    def invalidate_cache(self) -> None:
        """수동 cache invalidation. profiles/models 변경 시 호출."""
        self._cache = {}
        self._cache_loaded_at = 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_resolve = sub.add_parser("resolve")
    p_resolve.add_argument("profile")
    p_resolve.add_argument("--format", choices=["json", "text"], default="text")

    p_fb = sub.add_parser("fallback")
    p_fb.add_argument("profile")

    sub.add_parser("invalidate")
    sub.add_parser("list")

    args = ap.parse_args()
    resolver = LLMResolver()

    if args.cmd == "resolve":
        try:
            spec = resolver.resolve(args.profile)
        except (ValueError, FileNotFoundError) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        if args.format == "json":
            print(json.dumps(spec.to_dict(), ensure_ascii=False))
        else:
            print(f"profile={args.profile}")
            print(f"  alias={spec.alias}")
            print(f"  provider={spec.provider}")
            print(f"  cost_tier={spec.cost_tier}")
            print(f"  fallback={spec.fallback}")
        return 0
    elif args.cmd == "fallback":
        try:
            chain = resolver.fallback_chain(args.profile)
        except (ValueError, FileNotFoundError) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        for spec in chain:
            print(f"{spec.alias} ({spec.cost_tier})")
        return 0
    elif args.cmd == "invalidate":
        resolver.invalidate_cache()
        print("cache invalidated")
        return 0
    elif args.cmd == "list":
        resolver._load()
        print(json.dumps({
            "profiles": resolver._config.get("profiles", {}),
            "models": {k: v.to_dict() for k, v in resolver._cache.items()},
        }, ensure_ascii=False, indent=2))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
