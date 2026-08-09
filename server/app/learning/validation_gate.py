from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ValidationReport:
    passed: bool
    score: float
    checks: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ValidationGate:
    """
    Safety gate for evolution proposals.

    A proposal can be considered validated only when its checks pass.
    This component reports validation; it does not modify production code.
    """

    def evaluate(
        self,
        *,
        syntax_ok: bool,
        tests_ok: bool,
        regression_ok: bool,
        improvement_verified: bool,
    ) -> ValidationReport:
        checks = []
        failures = []

        results = {
            "syntax": syntax_ok,
            "tests": tests_ok,
            "regression": regression_ok,
            "improvement": improvement_verified,
        }

        for name, passed in results.items():
            if passed:
                checks.append(f"{name}:passed")
            else:
                failures.append(f"{name}:failed")

        score = sum(results.values()) / len(results)

        return ValidationReport(
            passed=not failures,
            score=score,
            checks=checks,
            failures=failures,
            metadata={
                "required_checks": list(results),
            },
        )
