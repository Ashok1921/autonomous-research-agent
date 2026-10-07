import json
from pathlib import Path


CHECKPOINT_DIR = Path("checkpoints")
RESEARCH_EVIDENCE_FILE = CHECKPOINT_DIR / "research_evidence.json"


def save_research_evidence(evidence) -> None:
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    data = []

    for item in evidence:
        if hasattr(item, "model_dump"):
            data.append(item.model_dump(mode="json"))
        else:
            data.append(item)

    with open(RESEARCH_EVIDENCE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(
        f"[Checkpoint] Saved {len(data)} research evidence items "
        f"to {RESEARCH_EVIDENCE_FILE}"
    )


def checkpoint_exists() -> bool:
    return RESEARCH_EVIDENCE_FILE.exists()


def load_research_evidence() -> list:
    if not checkpoint_exists():
        raise FileNotFoundError(
            f"Research checkpoint not found: {RESEARCH_EVIDENCE_FILE}"
        )

    with open(RESEARCH_EVIDENCE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)