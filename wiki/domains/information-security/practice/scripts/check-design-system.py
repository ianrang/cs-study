#!/usr/bin/env python3
"""Guard the static practice app's token, theme, and style-boundary contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINT = ROOT / "styles.css"
TOKEN_FILE = ROOT / "styles" / "tokens.css"
STYLE_LAYERS = [ROOT / "styles" / name for name in ("base.css", "components.css", "layout.css")]
HTML_FILE = ROOT / "index.html"
APP_FILE = ROOT / "app.js"
CORE_FILE = ROOT / "practice-core.js"

RAW_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(")
RAW_DIMENSION = re.compile(r"(?<![-\w])\d+(?:\.\d+)?(?:px|rem|em)\b")
INLINE_STYLE = re.compile(r"\bstyle\s*=|\.style\.|\.cssText\b|setAttribute\([^\n]*[\"']style[\"']")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    expected_imports = [
        '@import url("./styles/tokens.css") layer(tokens);',
        '@import url("./styles/base.css") layer(base);',
        '@import url("./styles/components.css") layer(components);',
        '@import url("./styles/layout.css") layer(layout);',
    ]
    entrypoint = read(ENTRYPOINT)
    import_positions: list[int] = []
    for expected in expected_imports:
        if expected not in entrypoint:
            errors.append(f"styles.css: missing ordered import: {expected}")
            continue
        import_positions.append(entrypoint.index(expected))
    if import_positions and import_positions != sorted(import_positions):
        errors.append("styles.css: token/base/component/layout imports are not in the required order")

    tokens = read(TOKEN_FILE)
    for required in (
        "color-scheme: light dark",
        'data-theme="light"',
        'data-theme="dark"',
        "light-dark(",
        "--color-text-primary",
        "--color-surface-panel",
        "--color-accent",
        "--color-focus-inner",
        "--color-focus-outer",
        "--color-status-success",
        "--space-",
        "--font-size-",
        "--radius-",
    ):
        if required not in tokens:
            errors.append(f"styles/tokens.css: required token/theme contract missing: {required}")
    for deprecated in ("--focus-ring-width", "--color-focus-ring"):
        if deprecated in tokens or any(deprecated in read(path) for path in STYLE_LAYERS):
            errors.append(f"deprecated focus token remains: {deprecated}")

    for path in [ENTRYPOINT, *STYLE_LAYERS]:
        content = read(path)
        if RAW_COLOR.search(content):
            errors.append(f"{path.relative_to(ROOT)}: raw color found outside token source")
        for line_number, line in enumerate(content.splitlines(), start=1):
            if line.lstrip().startswith("@media"):
                continue
            if RAW_DIMENSION.search(line):
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: raw dimension found outside token source")

    html = read(HTML_FILE)
    app = read(APP_FILE)
    core = read(CORE_FILE)
    for path, content in ((HTML_FILE, html), (APP_FILE, app), (CORE_FILE, core)):
        if INLINE_STYLE.search(content):
            errors.append(f"{path.relative_to(ROOT)}: inline or JavaScript style mutation found")
    for required in ("theme-toggle", "theme-toggle-label", "theme-current", "data-theme-storage-key", 'src="practice-core.js"'):
        if required not in html:
            errors.append(f"index.html: missing theme control contract: {required}")
    script_order = ['src="practice-data.js"', 'src="practice-core.js"', 'src="app.js"']
    script_positions = [html.find(script) for script in script_order]
    if -1 not in script_positions and script_positions != sorted(script_positions):
        errors.append("index.html: data, core, and app scripts are not loaded in dependency order")
    if 'id="theme-toggle" class="button button-quiet theme-toggle" type="button" aria-pressed=' in html:
        errors.append("index.html: theme cycle button must not use binary aria-pressed")
    for required in ("loadThemePreference", "getResolvedTheme", "renderThemeToggle", "toggleTheme", "restoreRequestedFocus"):
        if required not in app:
            errors.append(f"app.js: missing theme behavior contract: {required}")
    for required in ("isThemePreference", "nextThemePreference", "normalizeProgressRecord", "themePreferenceCycle"):
        if required not in core:
            errors.append(f"practice-core.js: missing theme state-machine contract: {required}")
    if 'class="stat surface surface-stat"' not in html:
        errors.append("index.html: statistic cards must compose the Surface contract")

    components = read(ROOT / "styles" / "components.css")
    stat_match = re.search(r"\.stat\s*\{(?P<body>.*?)\n\s*\}", components, re.DOTALL)
    if not stat_match:
        errors.append("styles/components.css: missing stat component contract")
    elif re.search(r"\b(background|border|border-radius|box-shadow)\s*:", stat_match.group("body")):
        errors.append("styles/components.css: stat must compose Surface instead of owning panel visuals")
    if "button:disabled" not in read(ROOT / "styles" / "base.css"):
        errors.append("styles/base.css: button disabled state is not styled")
    for selector in (
        ".surface",
        ".surface-stat",
        ".button",
        ".button-primary",
        ".button-quiet",
        ".button-danger",
        ".theme-toggle",
        ".badge-official",
        ".badge-source-derived",
        ".badge-inferred",
        ".badge-past-exam",
        ".badge-predicted",
        ".badge-attempted",
        ".badge-mastered",
        ".badge-review",
        ".question-step-unseen",
        ".question-step-attempted",
        ".question-step-mastered",
        ".question-step-review",
        ".feedback-correct",
        ".feedback-incorrect",
        ".feedback-self",
    ):
        if selector not in components:
            errors.append(f"styles/components.css: missing component variant: {selector}")

    if errors:
        print("design-system check failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("design-system check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
