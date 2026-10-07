from pathlib import Path

from app.models.final_report import FinalResearchReport


def save_report(
    report: FinalResearchReport,
    filename: str = "final_report.json",
):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # --------------------------------------
    # Save JSON report
    # --------------------------------------

    json_path = reports_dir / filename

    with open(json_path, "w", encoding="utf-8") as file:
        import json

        json.dump(
            report.model_dump(),
            file,
            indent=4,
            ensure_ascii=False,
        )

    # --------------------------------------
    # Save Markdown report
    # --------------------------------------

    markdown_path = reports_dir / "final_report.md"

    with open(markdown_path, "w", encoding="utf-8") as file:
        file.write(f"# {report.title}\n\n")

        file.write("## Executive Summary\n\n")
        file.write(f"{report.executive_summary}\n\n")

        file.write("## Key Findings\n\n")
        for item in report.key_findings:
            file.write(f"- {item}\n")
        file.write("\n")

        file.write("## Verified Facts\n\n")
        for item in report.verified_facts:
            file.write(f"- {item}\n")
        file.write("\n")

        file.write("## Uncertain / Partial Findings\n\n")
        for item in report.uncertain_or_partial_findings:
            file.write(f"- {item}\n")
        file.write("\n")

        file.write("## Contradicted Claims\n\n")
        for item in report.contradicted_claims:
            file.write(f"- {item}\n")
        file.write("\n")

        file.write("## Opportunities\n\n")
        for item in report.opportunities:
            file.write(f"- {item}\n")
        file.write("\n")

        file.write("## Challenges\n\n")
        for item in report.challenges:
            file.write(f"- {item}\n")
        file.write("\n")

        file.write("## Future Outlook\n\n")
        file.write(f"{report.future_outlook}\n\n")

        file.write("## Conclusion\n\n")
        file.write(f"{report.conclusion}\n\n")

        file.write("## Sources\n\n")
        for source in report.sources:
            file.write(f"- {source}\n")

    return json_path