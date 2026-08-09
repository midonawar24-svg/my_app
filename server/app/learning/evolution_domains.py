from pathlib import Path
from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvolutionDomain:
    domain_id: str
    name: str
    parent_id: str | None = None
    protected: bool = False
    children: tuple[str, ...] = field(default_factory=tuple)


ROOT_DOMAIN = EvolutionDomain(
    domain_id="project",
    name="Project",
    children=(
        "ai",
        "memory",
        "learning",
        "performance",
        "api",
        "ui",
    ),
)


DOMAINS = {
    "project": ROOT_DOMAIN,

    "ai": EvolutionDomain(
        domain_id="ai",
        name="Artificial Intelligence",
        parent_id="project",
        children=(
            "ai.local",
            "ai.providers",
            "ai.runtime",
        ),
    ),

    "ai.local": EvolutionDomain(
        domain_id="ai.local",
        name="Local AI",
        parent_id="ai",
    ),

    "ai.providers": EvolutionDomain(
        domain_id="ai.providers",
        name="AI Providers",
        parent_id="ai",
    ),

    "ai.runtime": EvolutionDomain(
        domain_id="ai.runtime",
        name="Model Runtime",
        parent_id="ai",
    ),

    "memory": EvolutionDomain(
        domain_id="memory",
        name="Memory",
        parent_id="project",
        children=(
            "memory.storage",
            "memory.retrieval",
            "memory.interests",
            "memory.personal",
        ),
    ),

    "memory.storage": EvolutionDomain(
        domain_id="memory.storage",
        name="Memory Storage",
        parent_id="memory",
    ),

    "memory.retrieval": EvolutionDomain(
        domain_id="memory.retrieval",
        name="Memory Retrieval",
        parent_id="memory",
    ),

    "memory.interests": EvolutionDomain(
        domain_id="memory.interests",
        name="Interests",
        parent_id="memory",
    ),

    "memory.personal": EvolutionDomain(
        domain_id="memory.personal",
        name="Personal Data",
        parent_id="memory",
        protected=True,
    ),

    "learning": EvolutionDomain(
        domain_id="learning",
        name="Learning",
        parent_id="project",
    ),

    "performance": EvolutionDomain(
        domain_id="performance",
        name="Performance",
        parent_id="project",
    ),

    "api": EvolutionDomain(
        domain_id="api",
        name="API",
        parent_id="project",
    ),

    "ui": EvolutionDomain(
        domain_id="ui",
        name="User Interface",
        parent_id="project",
    ),
}


def get_domain(domain_id: str) -> EvolutionDomain:
    try:
        return DOMAINS[domain_id]
    except KeyError as exc:
        raise ValueError(f"Unknown evolution domain: {domain_id}") from exc

def discover_subdomains(
    root: Path,
    parent_domain_id: str,
) -> dict[str, EvolutionDomain]:
    """
    Discover filesystem-backed subdomains recursively.

    Directories become evolution scopes.
    Protected domains and everything below them remain protected.
    """

    parent = DOMAINS.get(parent_domain_id)

    if parent is None:
        parent = EvolutionDomain(
            domain_id=parent_domain_id,
            name=parent_domain_id.rsplit(".", 1)[-1].replace("_", " ").title(),
            parent_id=parent_domain_id.rsplit(".", 1)[0]
            if "." in parent_domain_id
            else None,
            protected=False,
        )

    if parent.protected:
        return {}

    if not root.exists() or not root.is_dir():
        return {}

    discovered: dict[str, EvolutionDomain] = {}

    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue

        if child.name.startswith(".") or child.name == "__pycache__":
            continue

        domain_id = f"{parent_domain_id}.{child.name}"

        discovered[domain_id] = EvolutionDomain(
            domain_id=domain_id,
            name=child.name.replace("_", " ").title(),
            parent_id=parent_domain_id,
            protected=False,
        )

    return discovered
