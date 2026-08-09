from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionFileMapping:
    domain_id: str
    files: tuple[str, ...]


FILE_MAPPINGS = (
    EvolutionFileMapping(
        domain_id="memory",
        files=(
            "app/memory/__init__.py",
            "app/memory/gateway.py",
            "app/memory/models.py",
            "app/memory/in_memory_gateway.py",
            "app/memory/fake_gateway.py",
            "app/learning/memory_bridge.py",
            "app/learning/memory_sink.py",
        ),
    ),
    EvolutionFileMapping(
        domain_id="ai.local",
        files=(
            "app/providers/local_provider.py",
            "app/services/local_ai_config.py",
            "app/services/local_ai_runner.py",
        ),
    ),
    EvolutionFileMapping(
        domain_id="learning",
        files=(
            "app/learning/engine.py",
            "app/learning/models.py",
            "app/learning/pipeline.py",
            "app/learning/validator.py",
            "app/learning/validation_gate.py",
        ),
    ),
    EvolutionFileMapping(
        domain_id="api",
        files=(
            "app/api/__init__.py",
            "app/api/v1/__init__.py",
            "app/api/v1/chat.py",
            "app/api/v1/health.py",
        ),
    ),
)


def files_for_domain(domain_id: str) -> tuple[str, ...]:
    result: list[str] = []

    for mapping in FILE_MAPPINGS:
        if mapping.domain_id == domain_id:
            result.extend(mapping.files)

    return tuple(dict.fromkeys(result))

def discover_files_for_domain(
    project_root: Path,
    domain_id: str,
) -> tuple[str, ...]:
    """
    Discover Python files belonging to a filesystem-backed domain.
    """
    parts = domain_id.split(".")
    if not parts:
        return ()

    domain_path = project_root / "app" / parts[0]

    for part in parts[1:]:
        domain_path /= part

    if not domain_path.exists() or not domain_path.is_dir():
        return ()

    files: list[str] = []

    for path in sorted(domain_path.rglob("*.py")):
        if not path.is_file():
            continue

        if "__pycache__" in path.parts:
            continue

        files.append(
            str(path.relative_to(project_root))
        )

    return tuple(files)
