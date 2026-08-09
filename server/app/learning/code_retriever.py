from dataclasses import dataclass
from pathlib import Path

from app.learning.evolution_domains import (
    DOMAINS,
    EvolutionDomain,
    discover_subdomains,
)
from app.learning.evolution_file_map import (
    discover_files_for_domain,
    files_for_domain,
)


@dataclass(frozen=True)
class CodeRetrievalResult:
    domain_id: str
    domain_ids: tuple[str, ...]
    files: tuple[str, ...]
    protected_domains: tuple[str, ...]


class CodeRetriever:
    """
    Read-only code/domain discovery layer.

    Combines explicit file mappings with filesystem-backed
    subdomain discovery.

    It never modifies or executes project code.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()

    def _build_domains(self) -> dict[str, EvolutionDomain]:
        domains = dict(DOMAINS)

        interests_root = (
            self.project_root
            / "app"
            / "memory"
            / "interests"
        )

        def discover_recursive(
            root: Path,
            parent_domain_id: str,
        ) -> None:
            discovered = discover_subdomains(
                root,
                parent_domain_id,
            )

            for domain_id, domain in discovered.items():
                domains[domain_id] = domain

                parent = domains[parent_domain_id]

                if domain_id not in parent.children:
                    domains[parent_domain_id] = EvolutionDomain(
                        domain_id=parent.domain_id,
                        name=parent.name,
                        parent_id=parent.parent_id,
                        protected=parent.protected,
                        children=parent.children + (domain_id,),
                    aliases=parent.aliases,
                    )

                discover_recursive(
                    root / domain_id.rsplit(".", 1)[-1],
                    domain_id,
                )

        discover_recursive(
            interests_root,
            "memory.interests",
        )

        return domains

    def resolve_domains(self, domain_id: str) -> tuple[str, ...]:
        domains = self._build_domains()

        if domain_id not in domains:
            raise ValueError(
                f"Unknown evolution domain: {domain_id}"
            )

        result: list[str] = []

        def visit(current_id: str) -> None:
            result.append(current_id)

            for child_id in domains[current_id].children:
                visit(child_id)

        visit(domain_id)
        return tuple(result)

    def retrieve(self, domain_id: str) -> CodeRetrievalResult:
        domains = self._build_domains()
        domain_ids = self.resolve_domains(domain_id)

        protected = tuple(
            current_id
            for current_id in domain_ids
            if domains[current_id].protected
        )

        files: list[str] = []

        for current_id in domain_ids:
            for file_path in files_for_domain(current_id):
                if file_path not in files:
                    files.append(file_path)

            for file_path in discover_files_for_domain(
                self.project_root,
                current_id,
            ):
                if file_path not in files:
                    files.append(file_path)

        return CodeRetrievalResult(
            domain_id=domain_id,
            domain_ids=domain_ids,
            files=tuple(files),
            protected_domains=protected,
        )
