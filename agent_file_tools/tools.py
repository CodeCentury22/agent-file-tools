import os
from pathlib import Path
from typing import Dict, Any, List
from agent_core_utils import track_latency, audit_logger

def normalize_path(path_str: str) -> str:
    """Converts input path to an absolute, cross-platform POSIX path string."""
    return Path(path_str).resolve().as_posix()


@track_latency
@audit_logger(log_file="file_tools_telemetry.jsonl")
def read_file(file_path: str) -> Dict[str, Any]:
    """Reads and returns text content from a specified file."""
    try:
        posix_path = normalize_path(file_path)
        with open(posix_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "file_path": posix_path,
            "content": content,
            "status": "SUCCESS"
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "error": str(e),
            "status": "ERROR"
        }


@track_latency
@audit_logger(log_file="file_tools_telemetry.jsonl")
def write_file(file_path: str, code_body: str, overwrite: bool = True) -> Dict[str, Any]:
    """Writes content to a file, creating parent directories if needed."""
    try:
        path_obj = Path(file_path).resolve()
        posix_path = path_obj.as_posix()

        if path_obj.exists() and not overwrite:
            return {
                "file_path": posix_path,
                "error": "File exists and overwrite is set to False.",
                "status": "DENIED"
            }

        path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(path_obj, "w", encoding="utf-8") as f:
            f.write(code_body)

        return {
            "file_path": posix_path,
            "bytes_written": len(code_body.encode("utf-8")),
            "status": "SUCCESS"
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "error": str(e),
            "status": "ERROR"
        }


@track_latency
@audit_logger(log_file="file_tools_telemetry.jsonl")
def delete_file(file_path: str) -> Dict[str, Any]:
    """Deletes a file if it exists."""
    try:
        path_obj = Path(file_path).resolve()
        posix_path = path_obj.as_posix()

        if not path_obj.exists():
            return {
                "file_path": posix_path,
                "error": "File does not exist.",
                "status": "ERROR"
            }

        path_obj.unlink()
        return {
            "file_path": posix_path,
            "status": "SUCCESS"
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "error": str(e),
            "status": "ERROR"
        }


@track_latency
@audit_logger(log_file="file_tools_telemetry.jsonl")
def list_files(directory: str = ".") -> Dict[str, Any]:
    """Lists all files in a target directory."""
    try:
        dir_obj = Path(directory).resolve()
        posix_dir = dir_obj.as_posix()

        files = [p.name for p in dir_obj.iterdir()]
        return {
            "directory": posix_dir,
            "files": files,
            "status": "SUCCESS"
        }
    except Exception as e:
        return {
            "directory": directory,
            "error": str(e),
            "status": "ERROR"
        }


# =====================================================================
# Function Calling Schemas & Dispatcher
# =====================================================================

FILE_TOOLS_SCHEMA: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads and returns text content from a specified file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Target file path."}
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to a file, creating parent directories if needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Target file path."},
                    "code_body": {"type": "string", "description": "Text or code body to write."},
                    "overwrite": {"type": "boolean", "description": "Whether to overwrite existing files.", "default": True}
                },
                "required": ["file_path", "code_body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Deletes a file at the target path if it exists.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Target file path to remove."}
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lists all files in a target directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Target directory path.", "default": "."}
                },
                "required": []
            }
        }
    }
]

TOOL_DISPATCHER = {
    "read_file": read_file,
    "write_file": write_file,
    "delete_file": delete_file,
    "list_files": list_files,
}