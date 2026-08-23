import os
from pathlib import Path
from typing import Dict, Any
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
@audit_logger(log_file="file_tools_telemetry.jsonl")  # Fixed typo: telemtry -> telemetry
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

        # Create parent directories safely across OSs
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


@track_latency  # Fixed missing @ decorator symbol
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