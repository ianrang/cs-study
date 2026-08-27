#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import stat
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from knowledge.artifacts import (  # noqa: E402
    ArtifactError,
    capture,
    capture_asset,
    verify_manifest,
)
from knowledge.check import check_target  # noqa: E402
from knowledge.documents import (  # noqa: E402
    PagePlanError,
    apply_page_write_plan,
    build_collection_add_member_plan,
    build_collection_reorder_plan,
    build_move_plan,
    build_promote_plan,
    build_synthesize_plan,
    page_plan_bytes,
    write_set_overrides,
)
from knowledge.fs import (  # noqa: E402
    fsync_directory,
    publish_bytes_no_replace,
    rename_path_no_replace,
    write_bytes_fsync,
)
from knowledge.migration import (  # noqa: E402
    apply_resolved_plan,
    build_migration_plan,
    build_preservation_plan,
    build_reference_cascade_plan,
    create_backup,
    load_preservation_resolution,
    plan_bytes,
    preservation_capture_requests,
    preview_resolved_plan,
    recover_transaction,
    restore_backup,
    verify_backup,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="cs-study immutable knowledge pipeline"
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    capture_parser = subcommands.add_parser(
        "capture", help="capture one exact artifact"
    )
    capture_parser.add_argument("artifact", type=Path)
    capture_parser.add_argument("--source-type", required=True)
    capture_parser.add_argument("--source-id", required=True)
    capture_parser.add_argument("--primary-source", required=True)
    capture_parser.add_argument("--media-type", required=True)
    capture_parser.add_argument(
        "--now", default=None, help="normalized ISO 8601 activity time"
    )
    capture_parser.add_argument("--raw-root", type=Path, default=REPO_ROOT / "raw")

    asset_parser = subcommands.add_parser(
        "capture-asset", help="capture one content-addressed asset"
    )
    asset_parser.add_argument("asset", type=Path)
    asset_parser.add_argument("--source-id", required=True)
    asset_parser.add_argument("--media-type", required=True)
    asset_parser.add_argument(
        "--now", default=None, help="normalized ISO 8601 activity time"
    )
    asset_parser.add_argument("--raw-root", type=Path, default=REPO_ROOT / "raw")

    check_parser = subcommands.add_parser(
        "check", help="validate a target knowledge tree"
    )
    check_mode = check_parser.add_mutually_exclusive_group(required=True)
    check_mode.add_argument("--all", action="store_true")
    check_mode.add_argument("--changed", action="store_true")
    check_parser.add_argument("--target-root", type=Path, required=True)
    check_parser.add_argument("--path", dest="paths", type=Path, action="append")
    check_parser.add_argument("--report", choices=("text", "jsonl"), default="text")

    synthesize_parser = subcommands.add_parser(
        "synthesize", help="plan or apply one semantic draft"
    )
    synthesize_mode = synthesize_parser.add_mutually_exclusive_group(required=True)
    synthesize_mode.add_argument("--semantic-plan", type=Path)
    synthesize_mode.add_argument("--apply-plan", type=Path)
    synthesize_parser.add_argument("--source", dest="sources", action="append")
    synthesize_parser.add_argument("--page-id")
    synthesize_parser.add_argument("--now")
    synthesize_parser.add_argument("--output", type=Path)
    synthesize_parser.add_argument("--confirm-plan-sha256")

    promote_parser = subcommands.add_parser(
        "promote", help="plan or apply one reviewed draft promotion"
    )
    promote_parser.add_argument("draft", type=Path, nargs="?")
    promote_parser.add_argument("--target-dir", type=Path)
    promote_parser.add_argument("--review-verdicts", type=Path)
    promote_parser.add_argument("--output", type=Path)
    promote_parser.add_argument("--apply-plan", type=Path)
    promote_parser.add_argument("--confirm-plan-sha256")
    promote_parser.add_argument("--review-approved", action="store_true")

    collection_parser = subcommands.add_parser(
        "collection", help="plan or apply one collection page change"
    )
    collection_commands = collection_parser.add_subparsers(
        dest="collection_command", required=True
    )
    add_member_parser = collection_commands.add_parser("add-member")
    add_member_parser.add_argument("collection", type=Path, nargs="?")
    add_member_parser.add_argument("member", nargs="?")
    add_member_order = add_member_parser.add_mutually_exclusive_group()
    add_member_order.add_argument("--before")
    add_member_order.add_argument("--after")
    add_member_order.add_argument("--order-by-id", action="store_true")
    add_member_parser.add_argument("--output", type=Path)
    add_member_parser.add_argument("--apply-plan", type=Path)
    add_member_parser.add_argument("--confirm-plan-sha256")

    reorder_parser = collection_commands.add_parser("reorder")
    reorder_parser.add_argument("collection", type=Path, nargs="?")
    reorder_parser.add_argument("--member", dest="members", action="append")
    reorder_parser.add_argument("--output", type=Path)
    reorder_parser.add_argument("--apply-plan", type=Path)
    reorder_parser.add_argument("--confirm-plan-sha256")

    move_parser = subcommands.add_parser(
        "move", help="plan or apply one same-lifecycle page move"
    )
    move_parser.add_argument("page", type=Path, nargs="?")
    move_parser.add_argument("target_dir", type=Path, nargs="?")
    move_parser.add_argument("--output", type=Path)
    move_parser.add_argument("--apply-plan", type=Path)
    move_parser.add_argument("--confirm-plan-sha256")

    migration_parser = subcommands.add_parser(
        "migrate-plan", help="produce a stable-ID/frontmatter no-write plan"
    )
    migration_parser.add_argument("--knowledge-root", type=Path, required=True)
    migration_parser.add_argument("--output", type=Path)

    preservation_capture_parser = subcommands.add_parser(
        "migrate-capture-preservation",
        help=(
            "capture privacy-normalized legacy pages from an approved "
            "preservation resolution"
        ),
    )
    preservation_capture_parser.add_argument("--resolution", type=Path, required=True)
    preservation_capture_parser.add_argument(
        "--knowledge-root", type=Path, required=True
    )

    resolution_parser = subcommands.add_parser(
        "migrate-resolve",
        help="render an approved preservation resolution into an exact resolved plan",
    )
    resolution_parser.add_argument("--resolution", type=Path, required=True)
    resolution_parser.add_argument("--knowledge-root", type=Path, required=True)
    resolution_parser.add_argument("--output", type=Path, required=True)

    preview_parser = subcommands.add_parser(
        "migrate-preview",
        help="materialize and check a resolved plan without applying it",
    )
    preview_parser.add_argument("--plan", type=Path, required=True)
    preview_parser.add_argument("--knowledge-root", type=Path, required=True)
    preview_parser.add_argument("--output", type=Path, required=True)

    cascade_parser = subcommands.add_parser(
        "migrate-cascade-plan",
        help="produce a content-bound external-reference no-write plan and diff",
    )
    cascade_parser.add_argument("--plan", type=Path, required=True)
    cascade_parser.add_argument("--knowledge-root", type=Path, required=True)
    cascade_parser.add_argument("--preview-root", type=Path, required=True)
    cascade_parser.add_argument("--output", type=Path, required=True)

    backup_parser = subcommands.add_parser(
        "migrate-backup", help="create an exact tree backup bound to a resolved plan"
    )
    backup_parser.add_argument("--plan", type=Path, required=True)
    backup_parser.add_argument("--knowledge-root", type=Path, required=True)
    backup_parser.add_argument("--output", type=Path, required=True)

    verify_backup_parser = subcommands.add_parser(
        "migrate-verify-backup",
        help="verify backup path, metadata, bytes, and plan binding",
    )
    verify_backup_parser.add_argument("--plan", type=Path, required=True)
    verify_backup_parser.add_argument("--knowledge-root", type=Path, required=True)
    verify_backup_parser.add_argument("--backup", type=Path, required=True)

    apply_parser = subcommands.add_parser(
        "migrate-apply", help="atomically apply an approved resolved migration plan"
    )
    apply_parser.add_argument("--plan", type=Path, required=True)
    apply_parser.add_argument("--knowledge-root", type=Path, required=True)
    apply_parser.add_argument("--backup", type=Path, required=True)
    apply_parser.add_argument("--confirm-plan-sha256", required=True)
    apply_parser.add_argument("--cascade-plan", type=Path, required=True)
    apply_parser.add_argument("--confirm-cascade-plan-sha256", required=True)
    apply_parser.add_argument("--journal", type=Path, required=True)

    restore_parser = subcommands.add_parser(
        "migrate-restore",
        help="atomically restore an exact backup after a matching apply",
    )
    restore_parser.add_argument("--plan", type=Path, required=True)
    restore_parser.add_argument("--knowledge-root", type=Path, required=True)
    restore_parser.add_argument("--backup", type=Path, required=True)
    restore_parser.add_argument("--confirm-current-tree-sha256", required=True)
    restore_parser.add_argument("--cascade-plan", type=Path, required=True)
    restore_parser.add_argument("--confirm-cascade-plan-sha256", required=True)
    restore_parser.add_argument("--journal", type=Path, required=True)

    recover_parser = subcommands.add_parser(
        "migrate-recover", help="recover or finalize an interrupted atomic migration"
    )
    recover_parser.add_argument("--journal", type=Path, required=True)
    recover_parser.add_argument("--plan", type=Path, required=True)
    recover_parser.add_argument("--knowledge-root", type=Path, required=True)
    recover_parser.add_argument("--confirm-plan-sha256", required=True)
    recover_parser.add_argument("--cascade-plan", type=Path)
    recover_parser.add_argument("--confirm-cascade-plan-sha256")
    return parser


def _check_migration_candidate(
    target_root: Path, repo_root: Path, canonical_paths: list[Path]
) -> None:
    result = check_target(
        target_root,
        repo_root=repo_root,
        mode="changed",
        changed_paths=canonical_paths,
    )
    if result.structural_verdict != "PASS":
        raise ValueError(
            "migration candidate failed structural check with "
            f"{len(result.findings)} findings"
        )


def _check_page_candidate(write_set: list[dict]) -> None:
    knowledge_root = REPO_ROOT / "wiki"
    result = check_target(
        knowledge_root,
        repo_root=REPO_ROOT,
        mode="all",
        overrides=write_set_overrides(knowledge_root, write_set),
        include_repository_contracts=False,
    )
    if result.structural_verdict != "PASS":
        raise PagePlanError(
            f"candidate failed structural check with {len(result.findings)} findings"
        )


def _publish_page_plan(output: Path | None, plan: dict) -> None:
    if output is None:
        raise PagePlanError("plan mode requires --output")
    created = publish_bytes_no_replace(output, page_plan_bytes(plan))
    print(f"{'planned' if created else 'existing'}: {output}")


def _apply_page_plan(args: argparse.Namespace, expected_operation: str) -> None:
    if args.apply_plan is None or args.confirm_plan_sha256 is None:
        raise PagePlanError(
            "apply mode requires --apply-plan and --confirm-plan-sha256"
        )
    changed = apply_page_write_plan(
        args.apply_plan,
        args.confirm_plan_sha256,
        repo_root=REPO_ROOT,
        knowledge_root=REPO_ROOT / "wiki",
        candidate_check=_check_page_candidate,
        expected_operation=expected_operation,
        review_approved=getattr(args, "review_approved", False),
    )
    print(f"{'applied' if changed else 'unchanged'}: {args.apply_plan}")


def _cascade_bundle_matches(destination: Path, expected: dict[str, bytes]) -> bool:
    try:
        destination_mode = destination.lstat().st_mode
    except OSError:
        return False
    if stat.S_ISLNK(destination_mode) or not stat.S_ISDIR(destination_mode):
        return False
    entries = list(destination.iterdir())
    if {path.name for path in entries} != set(expected):
        return False
    for name, data in expected.items():
        path = destination / name
        try:
            mode = path.lstat().st_mode
        except OSError:
            return False
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode) or path.read_bytes() != data:
            return False
    return True


def _publish_cascade_bundle(destination: Path, plan: bytes, diff: bytes) -> bool:
    expected = {
        "cascade-plan.json": plan,
        "full.diff": diff,
    }
    if destination.exists() or destination.is_symlink():
        if _cascade_bundle_matches(destination, expected):
            return False
        raise FileExistsError(f"existing cascade bundle differs: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent)
    )
    try:
        for name, data in expected.items():
            write_bytes_fsync(temporary / name, data)
        fsync_directory(temporary)
        try:
            rename_path_no_replace(temporary, destination)
        except FileExistsError:
            if _cascade_bundle_matches(destination, expected):
                return False
            raise
        fsync_directory(destination.parent)
        return True
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "capture":
            result = capture(
                args.artifact,
                source_type=args.source_type,
                source_id=args.source_id,
                primary_source=args.primary_source,
                media_type=args.media_type,
                created_at=args.now or _utc_now(),
                raw_root=args.raw_root,
            )
        elif args.command == "capture-asset":
            result = capture_asset(
                args.asset,
                source_id=args.source_id,
                media_type=args.media_type,
                created_at=args.now or _utc_now(),
                raw_root=args.raw_root,
            )
        elif args.command == "check":
            mode = "changed" if args.changed else "all"
            result = check_target(
                args.target_root,
                repo_root=REPO_ROOT,
                mode=mode,
                changed_paths=args.paths,
            )
            if args.report == "jsonl":
                for finding in result.findings:
                    print(json.dumps(finding, ensure_ascii=False, sort_keys=True))
                print(
                    json.dumps(
                        {"result": result.to_dict()}, ensure_ascii=False, sort_keys=True
                    )
                )
            else:
                for finding in result.findings:
                    print(
                        f"{finding['severity']} {finding['rule_id']} "
                        f"{finding['path']}:{finding['line']} "
                        f"[{finding['subject_id']}] {finding['message']}"
                    )
                print(
                    f"structural={result.structural_verdict} "
                    f"semantic_review={result.semantic_review} "
                    f"findings={len(result.findings)} mode={result.mode}"
                )
                print(f"exclusions={','.join(result.exclusions)}")
            return int(result.structural_verdict != "PASS")
        elif args.command == "synthesize":
            if args.apply_plan is not None:
                if any(
                    value is not None
                    for value in (args.sources, args.page_id, args.now, args.output)
                ):
                    raise PagePlanError(
                        "synthesize apply mode accepts only plan and confirmation"
                    )
                _apply_page_plan(args, "synthesize")
            else:
                if any(
                    value is None
                    for value in (
                        args.semantic_plan,
                        args.sources,
                        args.page_id,
                        args.now,
                        args.output,
                    )
                ) or args.confirm_plan_sha256 is not None:
                    raise PagePlanError(
                        "synthesize plan mode requires semantic plan, source, "
                        "page ID, now, and output"
                    )
                plan = build_synthesize_plan(
                    semantic_plan_path=args.semantic_plan,
                    source_paths=args.sources,
                    page_id=args.page_id,
                    now=args.now,
                    repo_root=REPO_ROOT,
                    knowledge_root=REPO_ROOT / "wiki",
                )
                _check_page_candidate(plan["write_set"])
                _publish_page_plan(args.output, plan)
            return 0
        elif args.command == "promote":
            if args.apply_plan is not None:
                if any(
                    value is not None
                    for value in (
                        args.draft,
                        args.target_dir,
                        args.review_verdicts,
                        args.output,
                    )
                ):
                    raise PagePlanError(
                        "promote apply mode accepts only plan, confirmation, "
                        "and review approval"
                    )
                _apply_page_plan(args, "promote")
            else:
                if (
                    args.draft is None
                    or args.target_dir is None
                    or args.review_verdicts is None
                    or args.output is None
                    or args.confirm_plan_sha256 is not None
                    or args.review_approved
                ):
                    raise PagePlanError(
                        "promote plan mode requires draft, target directory, and output"
                    )
                plan = build_promote_plan(
                    args.draft,
                    args.target_dir,
                    review_verdicts_path=args.review_verdicts,
                    repo_root=REPO_ROOT,
                    knowledge_root=REPO_ROOT / "wiki",
                )
                _check_page_candidate(plan["write_set"])
                _publish_page_plan(args.output, plan)
            return 0
        elif args.command == "collection":
            if args.apply_plan is not None:
                plan_values = [args.collection, args.output]
                if args.collection_command == "add-member":
                    plan_values.extend([args.member, args.before, args.after])
                    if args.order_by_id:
                        plan_values.append(True)
                else:
                    plan_values.append(args.members)
                if any(value is not None for value in plan_values):
                    raise PagePlanError(
                        "collection apply mode accepts only plan and confirmation"
                    )
                _apply_page_plan(args, f"collection-{args.collection_command}")
            elif args.collection_command == "add-member":
                if (
                    args.collection is None
                    or args.member is None
                    or args.output is None
                    or args.confirm_plan_sha256 is not None
                ):
                    raise PagePlanError(
                        "collection add-member plan mode requires collection, "
                        "member, order, and output"
                    )
                plan = build_collection_add_member_plan(
                    args.collection,
                    args.member,
                    before=args.before,
                    after=args.after,
                    order_by_id=args.order_by_id,
                    repo_root=REPO_ROOT,
                    knowledge_root=REPO_ROOT / "wiki",
                )
                _check_page_candidate(plan["write_set"])
                _publish_page_plan(args.output, plan)
            else:
                if (
                    args.collection is None
                    or args.members is None
                    or args.output is None
                    or args.confirm_plan_sha256 is not None
                ):
                    raise PagePlanError(
                        "collection reorder plan mode requires collection, "
                        "members, and output"
                    )
                plan = build_collection_reorder_plan(
                    args.collection,
                    args.members,
                    repo_root=REPO_ROOT,
                    knowledge_root=REPO_ROOT / "wiki",
                )
                _check_page_candidate(plan["write_set"])
                _publish_page_plan(args.output, plan)
            return 0
        elif args.command == "move":
            if args.apply_plan is not None:
                if any(
                    value is not None
                    for value in (args.page, args.target_dir, args.output)
                ):
                    raise PagePlanError(
                        "move apply mode accepts only plan and confirmation"
                    )
                _apply_page_plan(args, "move")
            else:
                if (
                    args.page is None
                    or args.target_dir is None
                    or args.output is None
                    or args.confirm_plan_sha256 is not None
                ):
                    raise PagePlanError(
                        "move plan mode requires page, target directory, and output"
                    )
                plan = build_move_plan(
                    args.page,
                    args.target_dir,
                    repo_root=REPO_ROOT,
                    knowledge_root=REPO_ROOT / "wiki",
                )
                _check_page_candidate(plan["write_set"])
                _publish_page_plan(args.output, plan)
            return 0
        elif args.command == "migrate-plan":
            plan = build_migration_plan(REPO_ROOT, args.knowledge_root)
            rendered = plan_bytes(plan)
            if args.output is None:
                sys.stdout.buffer.write(rendered)
            else:
                created = publish_bytes_no_replace(args.output, rendered)
                print(f"{'planned' if created else 'existing'}: {args.output}")
            return 0
        elif args.command == "migrate-capture-preservation":
            inventory = build_migration_plan(REPO_ROOT, args.knowledge_root)
            resolution = load_preservation_resolution(
                args.resolution, inventory, REPO_ROOT, args.knowledge_root
            )
            requests = preservation_capture_requests(
                resolution, REPO_ROOT, args.knowledge_root
            )
            manifests = [capture(**request).manifest_path for request in requests]
            print(
                json.dumps(
                    {"captured_or_verified": len(manifests)},
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
            return 0
        elif args.command == "migrate-resolve":
            inventory = build_migration_plan(REPO_ROOT, args.knowledge_root)
            resolution = load_preservation_resolution(
                args.resolution, inventory, REPO_ROOT, args.knowledge_root
            )
            rendered = plan_bytes(
                build_preservation_plan(
                    resolution,
                    inventory,
                    REPO_ROOT,
                    args.knowledge_root,
                    verify_manifest,
                )
            )
            created = publish_bytes_no_replace(args.output, rendered)
            print(f"{'resolved' if created else 'existing'}: {args.output}")
            return 0
        elif args.command == "migrate-preview":
            result = preview_resolved_plan(
                args.plan,
                args.output,
                REPO_ROOT,
                args.knowledge_root,
                _check_migration_candidate,
                verify_manifest,
            )
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        elif args.command == "migrate-cascade-plan":
            cascade, diff = build_reference_cascade_plan(
                args.plan,
                args.preview_root,
                REPO_ROOT,
                args.knowledge_root,
            )
            rendered = plan_bytes(cascade)
            created = _publish_cascade_bundle(args.output, rendered, diff)
            print(
                json.dumps(
                    {
                        "active_reference_occurrences": cascade[
                            "active_reference_occurrences"
                        ],
                        "diff": str(args.output / "full.diff"),
                        "historical_reference_occurrences": sum(
                            int(item["occurrences"])
                            for item in cascade["historical_exemptions"]
                        ),
                        "operations": len(cascade["operations"]),
                        "output": str(args.output / "cascade-plan.json"),
                        "bundle_created": created,
                        "staged_stale_reference_occurrences": cascade[
                            "staged_stale_reference_occurrences"
                        ],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
            return 0
        elif args.command == "migrate-backup":
            result = create_backup(
                args.plan, args.output, REPO_ROOT, args.knowledge_root
            )
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        elif args.command == "migrate-verify-backup":
            result = verify_backup(
                args.plan, args.backup, REPO_ROOT, args.knowledge_root
            )
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        elif args.command == "migrate-apply":
            result = apply_resolved_plan(
                args.plan,
                args.backup,
                REPO_ROOT,
                args.knowledge_root,
                args.confirm_plan_sha256,
                args.journal,
                _check_migration_candidate,
                verify_manifest,
                args.cascade_plan,
                args.confirm_cascade_plan_sha256,
            )
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        elif args.command == "migrate-restore":
            result = restore_backup(
                args.plan,
                args.backup,
                REPO_ROOT,
                args.knowledge_root,
                args.confirm_current_tree_sha256,
                args.journal,
                args.cascade_plan,
                args.confirm_cascade_plan_sha256,
            )
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        elif args.command == "migrate-recover":
            result = recover_transaction(
                args.journal,
                args.plan,
                args.confirm_plan_sha256,
                REPO_ROOT,
                args.knowledge_root,
                args.cascade_plan,
                args.confirm_cascade_plan_sha256,
            )
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        else:
            raise AssertionError(f"unhandled command: {args.command}")
    except (ArtifactError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    status = "captured" if result.created else "existing"
    print(f"{status}: {result.manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
