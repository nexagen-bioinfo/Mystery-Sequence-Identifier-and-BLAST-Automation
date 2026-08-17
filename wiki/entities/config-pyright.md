---
title: "Config: pyrightconfig.json"
type: entity
tags:
  - config/typechecking
  - tooling/pyright
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - pyrightconfig.json
  - Pyright Static Analysis Config
---

# Config: `pyrightconfig.json`

The **Pyright Configuration** file provides compiler and static type checking configurations for Python Language Server (LSP) and Pyright/Pylance inside VS Code or Antigravity IDE.

---

## Configuration Schema

```json
{
  "venvPath": ".",
  "venv": "venv",
  "pythonVersion": "3.14",
  "extraPaths": [
    "./venv/lib/python3.14/site-packages"
  ]
}
```

### Key Directives:
- **`venvPath` / `venv`**: Directs the type checker to the local project virtual environment (`./venv`).
- **`extraPaths`**: Ensures installed library stubs (such as `Bio` in Biopython and `pandas`) resolve without unresolved import diagnostics.
- **`pythonVersion`**: Targets modern Python 3.14 typing semantics.

---

## Related Documentation
- [[codebase-blast-pipeline]]
- [[config-requirements]]
- [[Pipeline-Architecture]]
