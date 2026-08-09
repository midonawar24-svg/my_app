import asyncio
from pathlib import Path

from app.services.local_ai_config import LocalAIConfig


class LocalAIRunner:
    def __init__(self, config: LocalAIConfig | None = None):
        self.config = config or LocalAIConfig.from_env()

    @property
    def cli_path(self) -> Path:
        return self.config.llama_root / "build" / "bin" / "llama-cli"

    async def generate(
        self,
        model: Path,
        prompt: str,
        *,
        max_tokens: int = 512,
    ) -> str:
        if not self.cli_path.is_file():
            raise RuntimeError(f"llama-cli not found: {self.cli_path}")

        if not model.is_file():
            raise RuntimeError(f"Model not found: {model}")

        process = await asyncio.create_subprocess_exec(
            str(self.cli_path),
            "-m",
            str(model),
            "-p",
            prompt,
            "-n",
            str(max_tokens),
            "-t",
            str(self.config.default_threads),
            "-c",
            str(self.config.context_size),
            "--no-display-prompt",
            "--single-turn",
            "--simple-io",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=120,
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise RuntimeError(
                "llama.cpp generation timed out after 120 seconds"
            )

        if process.returncode != 0:
            error = stderr.decode(errors="replace").strip()
            raise RuntimeError(
                f"llama.cpp failed with exit code "
                f"{process.returncode}: {error}"
            )

        return stdout.decode(errors="replace").strip()
