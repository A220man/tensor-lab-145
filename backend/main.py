from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any
import uvicorn
import ast
import os
from pathlib import Path


def get_type_annotation(arg: ast.arg) -> Optional[str]:
    """Extract type annotation from function argument."""
    if arg.annotation:
        try:
            return ast.unparse(arg.annotation)
        except Exception:
            return None
    return None


def get_default_value(arg: ast.arg, defaults: list, kw_defaults: list, arg_index: int, num_args: int) -> Any:
    """Extract default value for function argument."""
    # Positional defaults are at the end
    num_defaults = len(defaults)
    default_start = num_args - num_defaults
    if arg_index >= default_start:
        default_idx = arg_index - default_start
        try:
            return ast.unparse(defaults[default_idx])
        except Exception:
            return None
    # Keyword-only defaults
    if arg_index < len(kw_defaults) and kw_defaults[arg_index] is not None:
        try:
            return ast.unparse(kw_defaults[arg_index])
        except Exception:
            return None
    return None


def is_cli_decorator(decorator: ast.AST) -> bool:
    """Check if a decorator is a CLI framework decorator."""
    # Handle ast.Name (e.g., @command)
    if isinstance(decorator, ast.Name):
        return decorator.id in ("command", "run", "ArgumentParser", "Typer")
    # Handle ast.Attribute (e.g., @click.command, @app.command, @typer.run)
    if isinstance(decorator, ast.Attribute):
        attr_name = decorator.attr
        if attr_name in ("command", "run", "argument", "option"):
            return True
        # Check for click.command, click.group, typer.Typer, etc.
        if isinstance(decorator.value, ast.Name):
            module_name = decorator.value.id
            if module_name in ("click", "typer", "argparse") and attr_name in ("command", "group", "Typer", "ArgumentParser"):
                return True
    # Handle ast.Call (e.g., @click.command(), @app.command())
    if isinstance(decorator, ast.Call):
        return is_cli_decorator(decorator.func)
    return False


def get_decorator_name(decorator: ast.AST) -> Optional[str]:
    """Get a readable name for a decorator."""
    if isinstance(decorator, ast.Name):
        return decorator.id
    if isinstance(decorator, ast.Attribute):
        if isinstance(decorator.value, ast.Name):
            return f"{decorator.value.id}.{decorator.attr}"
        return decorator.attr
    if isinstance(decorator, ast.Call):
        return get_decorator_name(decorator.func)
    return None


def analyze_python_file(file_path: str) -> dict:
    """Analyze a Python file and extract functions, classes, and entry points."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        tree = ast.parse(content, filename=file_path)
    except Exception as e:
        return {"error": str(e), "functions": [], "classes": [], "entry_points": []}

    functions = []
    classes = []
    entry_points = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args_info = []
            num_args = len(node.args.args)
            for i, arg in enumerate(node.args.args):
                arg_info = {
                    "name": arg.arg,
                    "type": get_type_annotation(arg),
                    "default": get_default_value(arg, node.args.defaults, node.args.kw_defaults, i, num_args),
                }
                args_info.append(arg_info)

            returns_type = None
            if node.returns:
                try:
                    returns_type = ast.unparse(node.returns)
                except Exception:
                    pass

            decorators = [get_decorator_name(d) for d in node.decorator_list]
            has_cli_decorator = any(is_cli_decorator(d) for d in node.decorator_list)

            func_info = {
                "name": node.name,
                "args": args_info,
                "returns": returns_type,
                "docstring": ast.get_docstring(node),
                "lineno": node.lineno,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
                "decorators": decorators,
                "has_cli_decorator": has_cli_decorator,
            }
            functions.append(func_info)

            # Check for entry points (if __name__ == "__main__", CLI decorators, etc.)
            is_entry = (
                node.name == "main" or
                has_cli_decorator or
                (node.decorator_list and any(
                    isinstance(d, ast.Name) and d.id in ("click.command", "typer.run", "argparse.ArgumentParser")
                    for d in node.decorator_list
                ))
            )
            if is_entry:
                entry_points.append(func_info)

        elif isinstance(node, ast.ClassDef):
            class_info = {
                "name": node.name,
                "methods": [],
                "lineno": node.lineno,
                "docstring": ast.get_docstring(node),
            }
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    args_info = []
                    num_args = len(item.args.args)
                    for i, arg in enumerate(item.args.args):
                        arg_info = {
                            "name": arg.arg,
                            "type": get_type_annotation(arg),
                            "default": get_default_value(arg, item.args.defaults, item.args.kw_defaults, i, num_args),
                        }
                        args_info.append(arg_info)

                    returns_type = None
                    if item.returns:
                        try:
                            returns_type = ast.unparse(item.returns)
                        except Exception:
                            pass

                    method_info = {
                        "name": item.name,
                        "args": args_info,
                        "returns": returns_type,
                        "docstring": ast.get_docstring(item),
                        "lineno": item.lineno,
                        "is_async": isinstance(item, ast.AsyncFunctionDef),
                    }
                    class_info["methods"].append(method_info)
            classes.append(class_info)

    return {
        "functions": functions,
        "classes": classes,
        "entry_points": entry_points,
    }


def analyze_source_path(source_path: str, language: str = None) -> dict:
    """Analyze source code at a given path."""
    path = Path(source_path)
    if not path.exists():
        return {"error": f"Path does not exist: {source_path}", "functions": [], "commands": [], "entry_points": []}

    all_functions = []
    all_classes = []
    all_entry_points = []

    if path.is_file():
        if path.suffix == ".py":
            result = analyze_python_file(str(path))
            all_functions.extend(result.get("functions", []))
            all_classes.extend(result.get("classes", []))
            all_entry_points.extend(result.get("entry_points", []))
    elif path.is_dir():
        for py_file in path.rglob("*.py"):
            result = analyze_python_file(str(py_file))
            all_functions.extend(result.get("functions", []))
            all_classes.extend(result.get("classes", []))
            all_entry_points.extend(result.get("entry_points", []))

    # Generate CLI commands from entry points and functions
    commands = []
    seen_commands = set()
    for ep in all_entry_points:
        cmd_key = ep["name"]
        if cmd_key not in seen_commands:
            commands.append({
                "name": ep["name"],
                "description": ep.get("docstring", ""),
                "parameters": ep.get("args", []),
                "source": "entry_point",
            })
            seen_commands.add(cmd_key)

    # Also generate commands from top-level functions that look like CLI commands
    for func in all_functions:
        if func["name"].startswith("cmd_") or func["name"].startswith("do_"):
            cmd_key = func["name"]
            if cmd_key not in seen_commands:
                commands.append({
                    "name": func["name"],
                    "description": func.get("docstring", ""),
                    "parameters": func.get("args", []),
                    "source": "naming_convention",
                })
                seen_commands.add(cmd_key)
        # Also include functions with CLI decorators
        elif func.get("has_cli_decorator"):
            cmd_key = func["name"]
            if cmd_key not in seen_commands:
                commands.append({
                    "name": func["name"],
                    "description": func.get("docstring", ""),
                    "parameters": func.get("args", []),
                    "source": "cli_decorator",
                })
                seen_commands.add(cmd_key)

    return {
        "functions": all_functions,
        "classes": all_classes,
        "entry_points": all_entry_points,
        "commands": commands,
    }


app = FastAPI(title="tensor-lab-145 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "tensor-lab-145"

class AnalyzeRequest(BaseModel):
    source_path: str
    language: Optional[str] = None

class AnalyzeResponse(BaseModel):
    functions: list = []
    classes: list = []
    commands: list = []
    entry_points: list = []

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse()

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    result = analyze_source_path(request.source_path, request.language)
    return AnalyzeResponse(**result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
