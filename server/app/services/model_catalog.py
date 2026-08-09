from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LocalModel:
    name: str
    path: Path
    size_bytes: int


class ModelCatalog:
    def __init__(self, models_dir: Path):
        self.models_dir = models_dir

    def list_models(self) -> list[LocalModel]:
        if not self.models_dir.exists():
            return []

        models = []

        for path in sorted(self.models_dir.glob("*.gguf")):
            if path.is_file():
                models.append(
                    LocalModel(
                        name=path.stem,
                        path=path,
                        size_bytes=path.stat().st_size,
                    )
                )

        return models
