"""The daily job installs only the runtime dependencies (`uv sync --locked --no-dev`).

`grimstrade.run_daily` (the record step) and `grimstrade.intraday` (the `--intraday` step) must
therefore import nothing outside the standard library and pyproject `dependencies`. A dev-only
package (numpy, gymnasium, ...) imported anywhere they reach would pass CI, which installs `dev`,
and break the unattended run.
"""

import ast
import os
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
ENTRIES = ("grimstrade.run_daily", "grimstrade.intraday")


def _module_file(name: str) -> Path | None:
    base = SRC.joinpath(*name.split("."))
    for path in (base / "__init__.py", base.with_suffix(".py")):
        if path.is_file():
            return path
    return None


def _is_type_checking(test: ast.expr) -> bool:
    return (isinstance(test, ast.Name) and test.id == "TYPE_CHECKING") or (
        isinstance(test, ast.Attribute) and test.attr == "TYPE_CHECKING"
    )


def _imports(tree: ast.AST, package: str) -> list[str]:
    """Every module name an import statement anywhere in `tree` may load (function bodies
    included, `if TYPE_CHECKING:` blocks excluded: they never run)."""
    out: list[str] = []

    def visit(node: ast.AST) -> None:
        if isinstance(node, ast.If) and _is_type_checking(node.test):
            for stmt in node.orelse:
                visit(stmt)
            return
        if isinstance(node, ast.Import):
            out.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                parts = package.split(".")
                base = ".".join(parts[: len(parts) - node.level + 1])
                mod = f"{base}.{node.module}" if node.module else base
            else:
                mod = node.module or ""
            out.append(mod)
            # `from pkg import sub` may load the submodule pkg.sub.
            out.extend(f"{mod}.{alias.name}" for alias in node.names)
        for child in ast.iter_child_nodes(node):
            visit(child)

    visit(tree)
    return out


def _outside_imports() -> dict[str, set[str]]:
    """Top-level names of non-grimstrade imports reachable from ENTRIES -> importing modules."""
    seen: set[str] = set()
    todo = list(ENTRIES)
    found: dict[str, set[str]] = {}
    while todo:
        name = todo.pop()
        if name in seen:
            continue
        seen.add(name)
        # Importing a.b.c runs a/__init__ and a/b/__init__ first.
        parts = name.split(".")
        todo.extend(".".join(parts[:i]) for i in range(1, len(parts)))
        path = _module_file(name)
        if path is None:
            continue  # a name imported from a module, not a submodule
        package = name if path.name == "__init__.py" else name.rpartition(".")[0]
        for mod in _imports(ast.parse(path.read_text(), str(path)), package):
            top = mod.split(".")[0]
            if top == "grimstrade":
                todo.append(mod)
            elif top:
                found.setdefault(top, set()).add(name)
    assert {"grimstrade.run_daily", "grimstrade.gym", "grimstrade.strategies.presets"} <= seen
    return found


def _allowed_third_party() -> set[str]:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    names = set()
    for req in project["dependencies"]:
        name = req.split(";")[0]
        for sep in "<>=!~[ ":
            name = name.split(sep)[0]
        names.add(name.strip().lower().replace("-", "_"))
    return names


def test_the_daily_runner_imports_only_the_stdlib_and_runtime_dependencies() -> None:
    allowed = set(sys.stdlib_module_names) | {"__future__"} | _allowed_third_party()
    bad = {top: sorted(by) for top, by in _outside_imports().items() if top not in allowed}
    assert not bad, f"not stdlib and not in pyproject dependencies: {bad}"


def test_the_daily_runner_imports_with_no_site_packages() -> None:
    """The same at run time: `python -S` drops site-packages (where numpy and the other dev
    packages live), so only the stdlib and `src/` can be imported."""
    code = f"import sys; sys.path.insert(0, {str(SRC)!r}); import " + ", ".join(ENTRIES)
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    out = subprocess.run(
        [sys.executable, "-S", "-c", code], capture_output=True, text=True, env=env, check=False
    )
    assert out.returncode == 0, out.stderr


def test_the_daily_job_installs_and_runs_without_the_dev_group() -> None:
    lines = (ROOT / ".github" / "workflows" / "daily.yml").read_text().splitlines()
    uv = [line.strip() for line in lines if "uv sync" in line or "uv run" in line]
    uv = [line for line in uv if not line.startswith("#")]
    assert len(uv) == 3, uv  # one sync, the record run, the intraday run
    assert all("--no-dev" in line for line in uv), uv
    assert any("uv sync --locked --no-dev" in line for line in uv)
