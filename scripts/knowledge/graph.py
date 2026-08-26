from __future__ import annotations

from collections import defaultdict
from pathlib import Path

DIRECTED_RELATIONS = {"broader", "prerequisite-of", "followed-by"}


def _finding(
    rule_id: str, path: Path, subject: str, message: str, remediation: str
) -> dict:
    return {
        "rule_id": rule_id,
        "severity": "HIGH",
        "path": str(path),
        "line": 1,
        "subject_id": subject,
        "message": message,
        "remediation": remediation,
    }


def _cycle_nodes(edges: dict[str, set[str]]) -> set[str]:
    visiting: set[str] = set()
    visited: set[str] = set()
    cycle: set[str] = set()

    def visit(node: str, stack: list[str]) -> None:
        if node in visiting:
            cycle.update(stack[stack.index(node) :])
            return
        if node in visited:
            return
        visiting.add(node)
        stack.append(node)
        for target in sorted(edges.get(node, set())):
            visit(target, stack)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in sorted(edges):
        visit(node, [])
    return cycle


def inspect_graph(records: list[tuple[Path, dict]]) -> list[dict]:
    findings: list[dict] = []
    by_id: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    for path, instance in records:
        by_id[instance["id"]].append((path, instance))

    for page_id, matches in sorted(by_id.items()):
        if len(matches) > 1:
            for path, _ in matches:
                findings.append(
                    _finding(
                        "VR-KP-007",
                        path,
                        page_id,
                        f"duplicate page ID/basename resolves to {len(matches)} pages",
                        "choose one globally unique stable filename ID",
                    )
                )

    for path, instance in records:
        page_id = instance["id"]
        for target in instance["links"]:
            count = len(by_id.get(target, []))
            if count != 1:
                findings.append(
                    _finding(
                        "VR-KP-008",
                        path,
                        page_id,
                        f"wikilink target {target!r} resolves to {count} pages",
                        "link one existing globally unique page ID",
                    )
                )

        member_targets = [member["target"] for member in instance["members"]]
        if len(member_targets) != len(set(member_targets)):
            findings.append(
                _finding(
                    "VR-KP-011",
                    path,
                    page_id,
                    "collection contains duplicate member targets",
                    "keep each member once; row order alone owns sequence",
                )
            )

        seen_relations: set[tuple[str, str]] = set()
        for relation in instance["relations"]:
            edge = (relation["type"], relation["target"])
            if edge in seen_relations:
                findings.append(
                    _finding(
                        "VR-KP-012",
                        path,
                        page_id,
                        f"duplicate relation edge: {edge}",
                        "store one outgoing edge",
                    )
                )
            seen_relations.add(edge)
            if relation["target"] == page_id:
                findings.append(
                    _finding(
                        "VR-KP-012",
                        path,
                        page_id,
                        f"self relation is forbidden: {edge}",
                        "remove the self edge",
                    )
                )
            if relation["type"] == "related" and page_id > relation["target"]:
                findings.append(
                    _finding(
                        "VR-KP-012",
                        path,
                        page_id,
                        "related edge must be owned by lexicographically smaller ID: "
                        f"{relation['target']}",
                        "move the outgoing related edge to the smaller-ID page",
                    )
                )

    for relation_type in sorted(DIRECTED_RELATIONS):
        edges: dict[str, set[str]] = defaultdict(set)
        paths: dict[str, Path] = {}
        for path, instance in records:
            paths[instance["id"]] = path
            for relation in instance["relations"]:
                if relation["type"] == relation_type:
                    edges[instance["id"]].add(relation["target"])
        for page_id in sorted(_cycle_nodes(edges)):
            findings.append(
                _finding(
                    "VR-KP-013",
                    paths[page_id],
                    page_id,
                    f"{relation_type} graph contains a directed cycle",
                    "remove or redirect one edge in the reported cycle",
                )
            )
    return findings
