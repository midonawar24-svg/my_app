from pathlib import Path
from typing import Any

from app.learning.code_retriever import CodeRetriever
from app.learning.evolution_memory import EvolutionMemory
from app.learning.evolution_store import EvolutionStore
from app.learning.project_analyzer import ProjectAnalyzer
from app.learning.evolution_domains import DOMAINS, discover_subdomains


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
    ):
        self.project_root = project_root.resolve()

        self.project_analyzer = ProjectAnalyzer(self.project_root)

        store = EvolutionStore(evolution_history)
        self.evolution_memory = EvolutionMemory(store)

        self.code_retriever = CodeRetriever(self.project_root)

    def _build_domains(self) -> dict[str, Any]:
        domains = dict(DOMAINS)

        interests_root = (
            self.project_root
            / "app"
            / "memory"
            / "interests"
        )

        discovered = discover_subdomains(
            interests_root,
            "memory.interests",
        )

        domains.update(discovered)

        # Recursively discover nested filesystem domains.
        pending = list(discovered.values())

        while pending:
            parent = pending.pop(0)

            if parent.protected:
                continue

            parent_path = self.project_root / Path(
                parent.domain_id.replace(".", "/")
            )

            children = discover_subdomains(
                parent_path,
                parent.domain_id,
            )

            for child_id, child in children.items():
                if child_id not in domains:
                    domains[child_id] = child
                    pending.append(child)

        # Rebuild child relationships from discovered domains.
        for domain_id, domain in list(domains.items()):
            if not domain.children:
                children = tuple(
                    child_id
                    for child_id, child in domains.items()
                    if child.parent_id == domain_id
                )

                if children:
                    from dataclasses import replace

                    domains[domain_id] = replace(
                        domain,
                        children=tuple(sorted(children)),
                    )

        result: dict[str, Any] = {}

        for domain_id, domain in domains.items():
            files: tuple[str, ...] = ()

            if not domain.protected:
                try:
                    files = self.code_retriever.retrieve(
                        domain_id
                    ).files
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
