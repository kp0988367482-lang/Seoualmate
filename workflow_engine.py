"""Core workflow engine used by the local MCP automation server."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class WorkflowStepResult:
    step: str
    status: str
    notes: str
    output: dict[str, Any]


class WorkflowEngine:
    """Small deterministic automation workflow engine."""

    def __init__(self, reports_dir: Path | None = None) -> None:
        base_dir = Path(__file__).resolve().parent
        self.reports_dir = reports_dir or (base_dir / "reports" / "workflow")
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def run_daily_workflow(
        self,
        objective: str,
        mode: str = "demo",
        save_report: bool = True,
    ) -> dict[str, Any]:
        mode_normalized = mode.strip().lower()
        if mode_normalized not in {"demo", "production"}:
            raise ValueError("mode must be either 'demo' or 'production'")

        started_at = datetime.now(timezone.utc)
        run_id = started_at.strftime("%Y%m%d-%H%M%S")

        steps: list[WorkflowStepResult] = [
            self._run_step_discovery(objective, mode_normalized),
            self._run_step_content(objective, mode_normalized),
            self._run_step_product(objective, mode_normalized),
            self._run_step_marketing(objective, mode_normalized),
            self._run_step_reporting(objective, mode_normalized),
        ]

        completed_steps = sum(1 for step in steps if step.status == "completed")
        failed_steps = [step.step for step in steps if step.status != "completed"]

        finished_at = datetime.now(timezone.utc)
        report: dict[str, Any] = {
            "run_id": run_id,
            "objective": objective,
            "mode": mode_normalized,
            "started_at": started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "duration_seconds": round((finished_at - started_at).total_seconds(), 3),
            "status": "success" if not failed_steps else "partial",
            "summary": {
                "total_steps": len(steps),
                "completed_steps": completed_steps,
                "failed_steps": failed_steps,
                "next_action": "Review report and execute blockers",
            },
            "steps": [asdict(step) for step in steps],
        }

        if save_report:
            self._save_report(report)

        return report

    def list_reports(self, limit: int = 10) -> list[dict[str, Any]]:
        if limit < 1:
            raise ValueError("limit must be >= 1")

        files = sorted(self.reports_dir.glob("*.json"), reverse=True)
        results: list[dict[str, Any]] = []

        for file in files[:limit]:
            payload = json.loads(file.read_text(encoding="utf-8"))
            results.append(
                {
                    "run_id": payload.get("run_id"),
                    "status": payload.get("status"),
                    "mode": payload.get("mode"),
                    "objective": payload.get("objective"),
                    "finished_at": payload.get("finished_at"),
                    "path": str(file),
                }
            )

        return results

    def latest_report(self) -> dict[str, Any]:
        files = sorted(self.reports_dir.glob("*.json"), reverse=True)
        if not files:
            raise FileNotFoundError("No workflow reports found")
        return json.loads(files[0].read_text(encoding="utf-8"))

    def get_report(self, run_id: str) -> dict[str, Any]:
        target = self.reports_dir / f"{run_id}.json"
        if not target.exists():
            raise FileNotFoundError(f"Report not found for run_id: {run_id}")
        return json.loads(target.read_text(encoding="utf-8"))

    def _save_report(self, report: dict[str, Any]) -> None:
        run_id = report["run_id"]
        target = self.reports_dir / f"{run_id}.json"
        target.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    def _run_step_discovery(self, objective: str, mode: str) -> WorkflowStepResult:
        return WorkflowStepResult(
            step="discovery",
            status="completed",
            notes="Collected context and constraints for today.",
            output={
                "objective": objective,
                "priority_signals": ["user_feedback", "error_trends", "top_requests"],
                "mode": mode,
            },
        )

    def _run_step_content(self, objective: str, mode: str) -> WorkflowStepResult:
        channels = ["blog", "email", "social"]
        return WorkflowStepResult(
            step="content_pipeline",
            status="completed",
            notes="Prepared channel-ready copy drafts.",
            output={
                "channels": channels,
                "draft_count": len(channels) * (2 if mode == "demo" else 4),
                "objective": objective,
            },
        )

    def _run_step_product(self, objective: str, mode: str) -> WorkflowStepResult:
        return WorkflowStepResult(
            step="product_pipeline",
            status="completed",
            notes="Prepared feature specification and rollout checklist.",
            output={
                "feature_candidates": ["onboarding_v2", "billing_alerts"],
                "test_plan": "smoke + regression",
                "deployment_target": "staging" if mode == "demo" else "production",
            },
        )

    def _run_step_marketing(self, objective: str, mode: str) -> WorkflowStepResult:
        return WorkflowStepResult(
            step="marketing_pipeline",
            status="completed",
            notes="Prepared campaign plan with conversion checkpoints.",
            output={
                "campaigns": ["retargeting", "newsletter", "partner_outreach"],
                "expected_new_users": 30 if mode == "demo" else 120,
                "expected_mrr_delta": 300 if mode == "demo" else 1400,
            },
        )

    def _run_step_reporting(self, objective: str, mode: str) -> WorkflowStepResult:
        return WorkflowStepResult(
            step="reporting",
            status="completed",
            notes="Generated daily summary package.",
            output={
                "kpis": {
                    "dau": 2500 if mode == "demo" else 4200,
                    "mrr": 18000 if mode == "demo" else 24500,
                    "conversion_rate": 3.8 if mode == "demo" else 5.2,
                },
                "objective": objective,
            },
        )
