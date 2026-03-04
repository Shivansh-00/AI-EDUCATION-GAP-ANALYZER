from pathlib import Path
import json
import joblib
from datetime import datetime

REGISTRY_DIR = Path("backend/ml/models")
REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST = REGISTRY_DIR / "registry.json"


class ModelRegistry:
    def __init__(self):
        if not MANIFEST.exists():
            MANIFEST.write_text(json.dumps({"models": [], "active": None}, indent=2))

    def _read_manifest(self):
        return json.loads(MANIFEST.read_text())

    def _write_manifest(self, data):
        MANIFEST.write_text(json.dumps(data, indent=2))

    def register(self, model, metrics: dict, prefix: str = "model") -> str:
        manifest = self._read_manifest()
        version = f"{prefix}_v{len(manifest['models']) + 1}.pkl"
        path = REGISTRY_DIR / version
        joblib.dump(model, path)

        entry = {
            "version": version,
            "path": str(path),
            "metrics": metrics,
            "created_at": datetime.utcnow().isoformat(),
        }
        manifest["models"].append(entry)
        manifest["active"] = version
        self._write_manifest(manifest)
        return version

    def get_active_model(self):
        manifest = self._read_manifest()
        active = manifest.get("active")
        if not active:
            raise FileNotFoundError("No active model in registry")
        return joblib.load(REGISTRY_DIR / active)

    def rollback(self, version: str):
        manifest = self._read_manifest()
        if version not in [m["version"] for m in manifest["models"]]:
            raise ValueError("Unknown model version")
        manifest["active"] = version
        self._write_manifest(manifest)
