# Copyright 2026 Aman Karir
# SPDX-License-Identifier: Apache-2.0
# Part of Shadow AI Guard, https://github.com/AmanSK5/shadow-ai-guard

"""CLI entry point for ai-guard.

Usage:
    ai-guard scan                    Run all enabled scanners
    ai-guard scan --scanner entra    Run a specific scanner
    ai-guard mcp-scan <config>       Standalone MCP security assessment
    ai-guard registry                Show loaded AI service registry
    ai-guard discover                Keyword DNS sweep for unknown AI tools
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.text import Text

from ai_guard import __version__
from ai_guard.config import Config
from ai_guard.registry import Registry
from ai_guard.report import ReportGenerator
from ai_guard.utils.audit import log_mcp_scan, log_scan_complete, log_scan_start


console = Console()


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--config", "-c",
    type=click.Path(exists=True),
    default=None,
    help="ポリシー設定YAMLのパス（既定: ./policy.yaml）",
)
@click.option(
    "--env-file", "-e",
    type=click.Path(),
    default=".env",
    show_default=True,
    help="API認証情報を読み込む.envファイルのパス。",
)
@click.pass_context
def main(ctx, config, env_file):
    """AIミハル: 未把握のAI利用を検出し、MCPのセキュリティを評価します。"""
    # Auto-load .env file if it exists
    env_path = Path(env_file)
    if env_path.exists():
        # Check file permissions before loading
        from ai_guard.utils.auth import check_env_file_permissions
        perm_warning = check_env_file_permissions(str(env_path))
        if perm_warning:
            console.print(f"[yellow]{perm_warning}[/yellow]")

        load_dotenv(env_path, override=False)
        console.print(f"[dim]認証情報を読み込みました: {env_path}[/dim]")
    elif env_file != ".env":
        # Only warn if they explicitly specified a non-default path
        console.print(f"[yellow]環境設定ファイルが見つかりません: {env_path}[/yellow]")
    ctx.ensure_object(dict)

    if config:
        ctx.obj["config"] = Config.from_file(Path(config))
    else:
        # Try default locations
        for default_path in [Path("policy.yaml"), Path("ai-guard.yaml")]:
            if default_path.exists():
                ctx.obj["config"] = Config.from_file(default_path)
                break
        else:
            ctx.obj["config"] = Config.default()

    ctx.obj["registry"] = Registry()


@main.command()
@click.option(
    "--scanner", "-s",
    multiple=True,
    help="指定した検出ソースだけを実行します。複数回指定できます。",
)
@click.option(
    "--format", "-f", "output_format",
    type=click.Choice(["terminal", "json", "csv", "confluence"]),
    default="terminal",
    help="出力形式。",
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="出力先ファイルのパス（json/csv）。",
)
@click.option(
    "--demo",
    is_flag=True,
    default=False,
    help="合成サンプルデータで実行します（APIを呼び出しません）。",
)
@click.pass_context
def scan(ctx, scanner, output_format, output, demo):
    """未把握のAI利用を検出します。"""
    registry: Registry = ctx.obj["registry"]

    if demo:
        config = _load_demo_config()
        ctx.obj["config"] = config
    else:
        config = ctx.obj["config"]

    from ai_guard.scanners import ALL_SCANNERS

    # Demo mode: use fixture scanners
    if demo:
        from ai_guard.scanners.demo import load_demo_scanners

        console.print("\n[bold yellow]デモモードで実行中 — すべて合成サンプルデータです。[/bold yellow]\n")
        console.print(f"[bold]AIミハル v{__version__}[/bold]")
        console.print(f"ツールレジストリ: {registry.stats['total_services']}件のAIツール")

        demo_scanners = load_demo_scanners(registry)
        scanner_names = [s.name for s in demo_scanners]
        console.print(f"検出ソース: {', '.join(scanner_names)}\n")

        log_scan_start(scanners=scanner_names, config_path="demo")

        results = []
        for scanner_instance in demo_scanners:
            ok, msg = scanner_instance.check_prerequisites()
            if not ok:
                console.print(f"  [yellow]⏭ {scanner_instance.name}: {msg}[/yellow]")
                from ai_guard.scanners.base import ScanResult
                results.append(ScanResult(scanner_name=scanner_instance.name, skipped_reason=msg))
                continue

            console.print(f"  [blue]⟳ {scanner_instance.name}: 検出中...[/blue]", end="")
            result = asyncio.run(scanner_instance.scan())
            results.append(result)
            console.print(f"\r  [green]✓ {scanner_instance.name}: 検出{result.finding_count}件（{result.duration_seconds:.1f}秒）[/green]")

    else:
        # Determine which scanners to run
        if scanner:
            scanner_names = list(scanner)
        else:
            scanner_names = [
                name for name, sconf in config.scanners.items()
                if sconf.enabled
            ]

        if not scanner_names:
            console.print(
                "[yellow]有効な検出ソースがありません。"
                "policy.yamlで有効にするか、--scannerで指定してください。[/yellow]\n"
                "利用できる検出ソース: " + ", ".join(ALL_SCANNERS.keys())
            )
            sys.exit(1)

        log_scan_start(scanners=scanner_names, config_path=str(ctx.parent.params.get("config") or "default"))

        console.print(f"\n[bold]AIミハル v{__version__}[/bold]")
        console.print(f"ツールレジストリ: {registry.stats['total_services']}件のAIツール")
        console.print(f"検出ソース: {', '.join(scanner_names)}\n")

        results = []

        for name in scanner_names:
            if name not in ALL_SCANNERS:
                console.print(f"[red]不明な検出ソース: {name}[/red]")
                continue

            scanner_cls = ALL_SCANNERS[name]
            scanner_config = config.scanners.get(name, config.scanners.get(name))

            if not scanner_config:
                from ai_guard.config import ScannerConfig
                scanner_config = ScannerConfig(enabled=True)

            scanner_instance = scanner_cls(registry=registry, config=scanner_config)

            # Check prerequisites
            ok, msg = scanner_instance.check_prerequisites()
            if not ok:
                console.print(f"  [yellow]⏭ {name}: {msg}[/yellow]")
                from ai_guard.scanners.base import ScanResult
                results.append(ScanResult(scanner_name=name, skipped_reason=msg))
                continue

            console.print(f"  [blue]⟳ {name}: 検出中...[/blue]", end="")

            result = asyncio.run(scanner_instance.scan())
            results.append(result)

            if result.errors:
                console.print(f"\r  [red]✗ {name}: 検出{result.finding_count}件、エラー{len(result.errors)}件[/red]")
            else:
                console.print(f"\r  [green]✓ {name}: 検出{result.finding_count}件（{result.duration_seconds:.1f}秒）[/green]")

    # Apply policy overrides to risk tiers
    for result in results:
        for finding in result.findings:
            override = config.policy.risk_overrides.get(finding.service.name)
            if override:
                finding.risk_tier = override

            if finding.service.name in config.policy.approved_services:
                finding.detail = f"[APPROVED] {finding.detail}"

            if finding.service.name in config.policy.blocked_services:
                finding.risk_tier = "high"
                finding.detail = f"[BLOCKED] {finding.detail}"

    # Generate report
    report = ReportGenerator(
        results=results,
        output_format=output_format,
    )
    report.generate(output_path=output)

    # Audit trail
    total_duration = sum(r.duration_seconds for r in results)
    log_scan_complete(
        scanners=scanner_names,
        finding_counts={r.scanner_name: r.finding_count for r in results},
        error_counts={r.scanner_name: len(r.errors) for r in results if r.errors},
        duration_seconds=total_duration,
        output_path=output,
    )


@main.command("mcp-scan")
@click.argument("config_path", type=click.Path(exists=True))
@click.pass_context
def mcp_scan(ctx, config_path):
    """MCPサーバーのセキュリティを個別に評価します。"""
    registry: Registry = ctx.obj["registry"]

    log_mcp_scan(config_path=config_path)

    from ai_guard.config import ScannerConfig
    from ai_guard.scanners.mcp import MCPScanner, RiskLevel, Verdict

    scanner = MCPScanner(
        registry=registry,
        config=ScannerConfig(enabled=True),
    )

    assessment = scanner.assess_from_file(Path(config_path))

    # Display assessment
    verdict_colors = {
        Verdict.BLOCK: "red",
        Verdict.ALLOW_WITH_CONDITIONS: "yellow",
        Verdict.ALLOW: "green",
    }

    console.print(f"\n[bold]MCPセキュリティ評価: {assessment.server_name}[/bold]")
    console.print(f"説明: {assessment.server_description}")
    console.print(f"認証方式: {assessment.auth_method}")
    console.print(f"ツール: 全{assessment.tool_count}件（読取り{len(assessment.read_tools)}件、書込み{len(assessment.write_tools)}件）")

    if assessment.oauth_scopes:
        console.print(f"OAuthスコープ: {', '.join(assessment.oauth_scopes)}")

    color = verdict_colors.get(assessment.verdict, "white")
    verdict_label = {"block": "禁止", "allow_with_conditions": "条件付き許可", "allow": "許可"}.get(assessment.verdict.value, assessment.verdict.value)
    console.print(f"\n[bold {color}]判定: {verdict_label}[/bold {color}]")

    if assessment.risks:
        console.print(f"\n[bold]リスク（{len(assessment.risks)}件）[/bold]")

        risk_table = Table(show_header=True, header_style="bold")
        risk_table.add_column("重大度")
        risk_table.add_column("分類")
        risk_table.add_column("リスク")
        risk_table.add_column("推奨する対応")

        level_colors = {
            RiskLevel.CRITICAL: "red bold",
            RiskLevel.HIGH: "red",
            RiskLevel.MEDIUM: "yellow",
            RiskLevel.LOW: "green",
            RiskLevel.INFO: "dim",
        }

        for risk in sorted(assessment.risks, key=lambda r: list(RiskLevel).index(r.level)):
            style = level_colors.get(risk.level, "white")
            risk_table.add_row(
                Text({"critical": "重大", "high": "高", "medium": "中", "low": "低", "info": "参考情報"}.get(risk.level.value, risk.level.value), style=style),
                risk.category,
                f"{risk.title}\n{risk.detail}",
                risk.recommendation,
            )

        console.print(risk_table)
    else:
        console.print("\n[green]リスクは検出されませんでした。[/green]")

    console.print()


@main.command()
@click.pass_context
def registry(ctx):
    """読み込んだツールレジストリを表示します。"""
    reg: Registry = ctx.obj["registry"]

    console.print(f"\n[bold]ツールレジストリ[/bold]")
    console.print(f"ツール数: {reg.stats['total_services']}")

    table = Table(show_header=True, header_style="bold")
    table.add_column("ツール")
    table.add_column("提供元")
    table.add_column("分類")
    table.add_column("リスク")
    table.add_column("ドメイン")
    table.add_column("検出方法")

    for svc in sorted(reg.services, key=lambda s: (s.risk_tier, s.name)):
        methods = []
        if svc.domains:
            methods.append("DNS")
        if svc.entra_app_ids:
            methods.append("Entra")
        if svc.email_domains:
            methods.append("メール")
        if svc.desktop_apps.get("windows") or svc.desktop_apps.get("macos"):
            methods.append("アプリ")
        if any(svc.browser_extensions.values()):
            methods.append("拡張機能")
        if svc.mcp_identifiers:
            methods.append("MCP")

        risk_color = RISK_COLORS.get(svc.risk_tier, "white")

        table.add_row(
            svc.name,
            svc.vendor,
            svc.category,
            Text({"high": "高", "medium": "中", "low": "低"}.get(svc.risk_tier, svc.risk_tier), style=risk_color),
            ", ".join(svc.domains[:2]) + ("..." if len(svc.domains) > 2 else ""),
            ", ".join(methods),
        )

    console.print(table)
    console.print()


@main.command()
@click.pass_context
def init(ctx):
    """現在のディレクトリにAIミハルの初期設定を作成します。

    テンプレートからアクセス権限を制限した.envを作成し、
    既定のpolicy.yamlをコピーします。
    """
    import shutil

    package_dir = Path(__file__).parent.parent

    # Create .env from template
    env_file = Path(".env")
    env_example = package_dir / ".env.example"

    if env_file.exists():
        console.print("[yellow].envが存在するため作成を省略します[/yellow]")
        # Still check permissions on existing file
        _secure_env_file(env_file)
    elif env_example.exists():
        shutil.copy(env_example, env_file)
        _secure_env_file(env_file)
        console.print("[green].envを権限600で作成しました。API認証情報を設定してください[/green]")
    else:
        console.print("[yellow]同梱の.env.exampleが見つかりません。.envを手動で作成してください[/yellow]")

    # Copy policy.yaml if not present
    policy_file = Path("policy.yaml")
    policy_template = package_dir / "policy.yaml"

    if policy_file.exists():
        console.print("[yellow]policy.yamlが存在するため作成を省略します[/yellow]")
    elif policy_template.exists():
        shutil.copy(policy_template, policy_file)
        console.print("[green]policy.yamlを作成しました。検出ソースとポリシーを設定してください[/green]")

    console.print(
        "\n[bold]次の手順:[/bold]\n"
        "  1. .envにAPI認証情報を設定します\n"
        "  2. policy.yamlで検出ソースを有効にし、禁止・承認するツールを設定します\n"
        "  3. 実行: ai-guard scan\n"
    )


def _secure_env_file(path: Path) -> None:
    """Set .env file to owner-only read/write (chmod 600)."""
    try:
        import stat
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except (OSError, AttributeError):
        pass  # Windows or permission error: skip


@main.command()
@click.option(
    "--lookback", "-l",
    type=int,
    default=14,
    show_default=True,
    help="DNS履歴を検索する日数（最大14日）。",
)
@click.pass_context
def discover(ctx, lookback):
    """DNSのキーワード検索で未登録のAIツールを探します。

    SentinelOne Deep VisibilityでAI関連キーワードを含むDNS検索を調べ、
    登録済みドメインと代表的な誤検出を除き、
    未登録のAIツール候補を観測回数順に表示します。

    AIGUARD_S1_BASE_URLとAIGUARD_S1_API_TOKENの設定が必要です。
    """
    from ai_guard.discover import AI_KEYWORDS, run_discover
    from ai_guard.utils.auth import AuthError, SentinelOneAuth

    registry: Registry = ctx.obj["registry"]

    # Authenticate
    try:
        auth = SentinelOneAuth.from_env("AIGUARD_S1")
    except AuthError as e:
        console.print(f"[red]{e}[/red]")
        sys.exit(1)

    console.print(f"\n[bold]AIミハル — 未登録ツールの探索[/bold]")
    console.print(f"キーワード: {', '.join(AI_KEYWORDS)}")
    console.print(f"検索期間: 過去{lookback}日間")
    console.print(f"ツールレジストリ: 登録済み{registry.stats['total_services']}件（{registry.stats['indexed_domains']}ドメインを除外）\n")
    console.print("[blue]SentinelOne Deep VisibilityでDNSのキーワード検索を実行しています...[/blue]")
    console.print("[dim]APIの呼出し回数制限により数分かかる場合があります。[/dim]\n")

    domain_counts, errors = asyncio.run(
        run_discover(auth=auth, registry=registry, lookback_days=lookback)
    )

    # Show errors if any
    if errors:
        console.print(f"[yellow]エラーが{len(errors)}件発生しました:[/yellow]")
        for err in errors:
            console.print(f"  [dim]{err}[/dim]")
        console.print()

    # Display results
    if not domain_counts:
        console.print("[green]未登録のAI関連ドメインは見つかりませんでした。[/green]\n")
        return

    console.print(f"[bold]未登録のAI関連ドメイン候補（重複を除いて{len(domain_counts)}件）:[/bold]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("ドメイン", style="cyan")
    table.add_column("観測回数", justify="right")

    for domain, count in domain_counts.most_common():
        table.add_row(domain, str(count))

    console.print(table)
    console.print(
        f"\n[dim]これらのドメインはAIキーワードに一致しましたが、ツールレジストリに未登録です。\n"
        f"確認後、AIツールと判断したものをai_services.yamlに追加してください。[/dim]\n"
    )


RISK_COLORS = {
    "high": "red",
    "medium": "yellow",
    "low": "green",
}


def _load_demo_config() -> Config:
    """Load the demo policy file bundled with the project."""
    demo_policy = Path(__file__).parent.parent / "policies" / "demo.yaml"
    if demo_policy.exists():
        return Config.from_file(demo_policy)
    # Fallback: default config with ChatGPT blocked, Copilot approved
    from ai_guard.config import PolicyConfig
    return Config(
        scanners={},
        policy=PolicyConfig(
            blocked_services=["ChatGPT"],
            approved_services=["GitHub Copilot"],
        ),
    )


if __name__ == "__main__":
    main()
