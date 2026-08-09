from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class LocalAIConfig:
    llama_root: Path
    models_dir: Path
    cache_dir: Path
    logs_dir: Path
    default_threads: int
    context_size: int

    @classmethod
    def from_env(cls) -> "LocalAIConfig":
        server_root = Path(__file__).resolve().parents[2]
        runtime_root = server_root / "ai_runtime"

        return cls(
            llama_root=Path(
                os.getenv("LLAMA_CPP_ROOT", str(Path.home() / "llama.cpp"))
            ),
            models_dir=Path(
                os.getenv("LOCAL_AI_MODELS_DIR", str(runtime_root / "models"))
            ),
            cache_dir=Path(
                os.getenv("LOCAL_AI_CACHE_DIR", str(runtime_root / "cache"))
            ),
            logs_dir=Path(
                os.getenv("LOCAL_AI_LOGS_DIR", str(runtime_root / "logs"))
            ),
            default_threads=int(os.getenv("LOCAL_AI_THREADS", "6")),
            context_size=int(os.getenv("LOCAL_AI_CONTEXT", "4096")),
        )
