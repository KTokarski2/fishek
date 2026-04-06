from services.decision_service import build_result_row, partition_decisions


# ---------------------------------------------------------------------------
# build_result_row
# ---------------------------------------------------------------------------

def test_build_result_row_full_evaluation():
    evaluation = {"accuracy": 9, "naturalness": 8, "fluency": 7, "notes": "Looks good"}
    row = build_result_row("cat", "english", "kot", evaluation)
    assert row == ["cat", "english", "kot", 9, 8, 7, "Looks good"]


def test_build_result_row_missing_evaluation_fields():
    row = build_result_row("cat", "english", "kot", {})
    assert row == ["cat", "english", "kot", "-", "-", "-", ""]


def test_build_result_row_partial_evaluation():
    evaluation = {"accuracy": 5, "notes": "Partial"}
    row = build_result_row("dog", "french", "chien", evaluation)
    assert row[3] == 5
    assert row[4] == "-"
    assert row[5] == "-"
    assert row[6] == "Partial"


# ---------------------------------------------------------------------------
# partition_decisions
# ---------------------------------------------------------------------------

def _rows(n):
    return [[f"word{i}"] for i in range(n)]


def test_partition_decisions_all_accept():
    rows = _rows(3)
    decisions = ["accept", "accept", "accept"]
    accepted, to_refine, dropped = partition_decisions(rows, decisions)
    assert accepted == rows
    assert to_refine == []
    assert dropped == []


def test_partition_decisions_all_refine():
    rows = _rows(3)
    decisions = ["refine", "refine", "refine"]
    accepted, to_refine, dropped = partition_decisions(rows, decisions)
    assert accepted == []
    assert to_refine == rows
    assert dropped == []


def test_partition_decisions_all_drop():
    rows = _rows(3)
    decisions = ["drop", "drop", "drop"]
    accepted, to_refine, dropped = partition_decisions(rows, decisions)
    assert accepted == []
    assert to_refine == []
    assert dropped == rows


def test_partition_decisions_mixed():
    rows = _rows(5)
    decisions = ["accept", "refine", "drop", "accept", "refine"]
    accepted, to_refine, dropped = partition_decisions(rows, decisions)
    assert accepted == [rows[0], rows[3]]
    assert to_refine == [rows[1], rows[4]]
    assert dropped == [rows[2]]


def test_partition_decisions_empty():
    accepted, to_refine, dropped = partition_decisions([], [])
    assert accepted == []
    assert to_refine == []
    assert dropped == []


def test_partition_decisions_preserves_order():
    rows = _rows(4)
    decisions = ["refine", "accept", "refine", "accept"]
    accepted, to_refine, _ = partition_decisions(rows, decisions)
    assert accepted == [rows[1], rows[3]]
    assert to_refine == [rows[0], rows[2]]
