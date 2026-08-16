import os
from typing import Dict, Any
from agent_core_utils import track_latency, audit_logger

@track_latency
@audit_logger(log_file="file_tools_telemetry.jsonl")
def read_file(file_path: str) -> Dict[str, Any]:
    """Reads and returns text content from a specified file."""
    try:
        normalized_path = os.path.normpath(file_path)
        with open(normalized_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "file_path": normalized_path,
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
@audit_logger(log_file="file_tools_telemtry.jsonl")
def write_file(file_path: str, code_body: str, overwrite: bool = True) -> Dict[str, Any]:
    """Writes content to a file, creating parent directories if needed."""
    try:
        normalized_path = os.path.normpath(file_path)

        if os.path.exists(normalized_path) and not overwrite:
            return {
                "file_path": normalized_path,
                "error": "File exists and overwrite is set to False.",
                "status": "DENIED"
            }

        dir_name = os.path.dirname(normalized_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(normalized_path, "w", encoding="utf-8") as f:
            f.write(code_body)

        return {
            "file_path": normalized_path,
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
        normalized_path = os.path.normpath(file_path)
        if not os.path.exists(normalized_path):
            return {
                "file_path": normalized_path,
                "error": "File does not exist.",
                "status": "ERROR"
            }
        os.remove(normalized_path)
        return {
            "file_path": normalized_path,
            "status": "SUCCESS"
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "error": str(e),
            "status": "ERROR"
        }

track_latency
@audit_logger(log_file="file_tools_telemetry.jsonl")
def list_files(directory: str = ".") -> Dict[str, Any]:
    """Lists all files in a target directory."""
    try:
        normalized_dir = os.path.normpath(directory)
        files = os.listdir(normalized_dir)
        return {
            "directory": normalized_dir,
            "files": files,
            "status": "SUCCESS"
        }
    except Exception as e:
        return {
            "directory": directory,
            "error": str(e),
            "status": "ERROR"
        }