from pathlib import Path
from typing import Any

from app.learning.code_retriever import CodeRetriever
from app.learning.evolution_memory import EvolutionMemory
from app.learning.evolution_store import EvolutionStore
from app.learning.project_analyzer import ProjectAnalyzer


class EvolutionContextBuilder:
    """
    Builds read-only context for the local AI.

    Includes:
    - project structure/statistics
    - evolution history
    - successful/failed patterns
    - static evolution domains
    - dynamically discovered domains
    - files belonging to each discovered domain

    This builder never modifies project code.
    """

    def __init__(
        self,
        project_root: Path,
        evolution_history: Path,
        discovery_roots: tuple[tuple[Path, str], ...] | None = None,
    ):
        self.project_root = project_root.resolve()

        self.project_analyzer = ProjectAnalyzer(self.project_root)

        store = EvolutionStore(evolution_history)
        self.evolution_memory = EvolutionMemory(store)

        self.code_retriever = CodeRetriever(
            self.project_root,
            discovery_roots=discovery_roots,
        )

    def _build_domains(self) -> dict[str, Any]:
        domains = self.code_retriever._build_domains()

        result: dict[str, Any] = {}

        for domain_id, domain in domains.items():
            files: tuple[str, ...] = ()

            if not domain.protected:
                try:
                    files = self.code_retriever.retrieve(domain_id).files
                except ValueError:
                    files = ()

            result[domain_id] = {
                "name": domain.name,
                "parent_id": domain.parent_id,
                "protected": domain.protected,
                "children": list(domain.children),
                "files": list(files),
            }

        return result

    def build(self) -> dict[str, Any]:
        project_context = (
            self.project_analyzer
            .analyze()
            .to_context()
        )

        evolution_context = (
            self.evolution_memory
            .build_context(limit=10)
        )

        return {
            **project_context,
            **evolution_context,
            "evolution_domains": self._build_domains(),
        }
