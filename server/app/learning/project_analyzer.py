from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectFile:
    path: str
    lines: int
    size_bytes: int


@dataclass(frozen=True)
class ProjectAnalysis:
    root: str
    files: list[ProjectFile]
    total_files: int
    total_lines: int
    total_bytes: int

    def to_context(self) -> dict:
        return {
            "project_analysis": {
                "root": self.root,
                "total_files": self.total_files,
                "total_lines": self.total_lines,
                "total_bytes": self.total_bytes,
                "files": [
                    {
                        "path": item.path,
                        "lines": item.lines,
                        "size_bytes": item.size_bytes,
                    }
                    for item in self.files
                ],
            }
        }


class ProjectAnalyzer:
    """
    Read-only project analyzer.

    It inspects source files and produces structured context.
    It never executes or modifies project code.
    """

    DEFAULT_EXTENSIONS = {
        ".py",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".md",
    }

    IGNORED_PARTS = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        "build",
        "dist",
    }

    def __init__(
        self,
        root: Path,
        extensions: set[str] | None = None,
    ):
        self.root = root.resolve()
        self.extensions = extensions or self.DEFAULT_EXTENSIONS

    def analyze(self) -> ProjectAnalysis:
        if not self.root.exists():
            raise FileNotFoundError(
                f"Project root does not exist: {self.root}"
            )

        files: list[ProjectFile] = []

        for path in sorted(self.root.rglob("*")):
            if not path.is_file():
                continue

            if any(part in self.IGNORED_PARTS for part in path.parts):
                continue

            if path.suffix.lower() not in self.extensions:
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            files.append(
                ProjectFile(
                    path=str(path.relative_to(self.root)),
                    lines=len(text.splitlines()),
                    size_bytes=path.stat().st_size,
                )
            )

        return ProjectAnalysis(
            root=str(self.root),
            files=files,
            total_files=len(files),
            total_lines=sum(item.lines for item in files),
            total_bytes=sum(item.size_bytes for item in files),
        )
