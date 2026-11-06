from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import ast
import os
from pathlib import Path


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
            func_info = {
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "returns": ast.unparse(node.returns) if node.returns else None,
                "docstring": ast.get_docstring(node),
                "lineno": node.lineno,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
            }
            functions.append(func_info)

            # Check for entry points (if __name__ == "__main__", CLI decorators, etc.)
            if node.name == "main" or (node.decorator_list and any(
                isinstance(d, ast.Name) and d.id in ("click.command", "typer.run", "argparse.ArgumentParser")
                for d in node.decorator_list
            )):
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
                    method_info = {
                        "name": item.name,
                        "args": [arg.arg for arg in item.args.args],
                        "returns": ast.unparse(item.returns) if item.returns else None,
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
    for ep in all_entry_points:
        commands.append({
            "name": ep["name"],
            "description": ep.get("docstring", ""),
            "parameters": ep.get("args", []),
            "source": "entry_point",
        })

    # Also generate commands from top-level functions that look like CLI commands
    for func in all_functions:
        if func["name"].startswith("cmd_") or func["name"].startswith("do_"):
            commands.append({
                "name": func["name"],
                "description": func.get("docstring", ""),
                "parameters": func.get("args", []),
                "source": "naming_convention",
            })

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
