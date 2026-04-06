def build_result_row(word: str, language: str, translation: str, evaluation: dict) -> list:
    return [
        word,
        language,
        translation,
        evaluation.get("accuracy", "-"),
        evaluation.get("naturalness", "-"),
        evaluation.get("fluency", "-"),
        evaluation.get("notes", ""),
    ]


def partition_decisions(results: list, decisions: list[str]) -> tuple[list, list, list]:
    accepted = [results[i] for i, d in enumerate(decisions) if d == "accept"]
    to_refine = [results[i] for i, d in enumerate(decisions) if d == "refine"]
    dropped = [results[i] for i, d in enumerate(decisions) if d == "drop"]
    return accepted, to_refine, dropped
