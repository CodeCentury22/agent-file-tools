# Agent File Tools 📁🛡️

File system operation wrappers with path normalization, telemetry logging, and guardrails for AI agents.

## Installation

Add agent-file-tools to your project using uv:

uv add git+[https://github.com/CodeCentury22/agent-file-tools.git@v0.1.0](https://github.com/CodeCentury22/agent-file-tools.git@v0.1.0)

## Quick Start

from agent_file_tools import read_file, write_file, delete_file, list_files

# 1. Write file with automatic parent directory creation
write_res = write_file("src/utils/helpers.py", "def greet(): return 'Hello'")
print(write_res["status"])  # 'SUCCESS'

# 2. Read file securely with path normalization
read_res = read_file("src/utils/helpers.py")
print(read_res["content"])  # "def greet(): return 'Hello'"

# 3. List contents of directory
list_res = list_files("src")
print(list_res["files"])  # ['utils']

# 4. Delete file
del_res = delete_file("src/utils/helpers.py")
print(del_res["status"])  # 'SUCCESS'

## API Reference

* read_file(file_path: str) -> Dict[str, Any]: Reads text content from a normalized file path.
* write_file(file_path: str, code_body: str, overwrite: bool = True) -> Dict[str, Any]: Writes content to disk, automatically creating missing parent directories. Returns DENIED if overwrite=False and the file exists.
* delete_file(file_path: str) -> Dict[str, Any]: Removes the specified file if it exists.
* list_files(directory: str = ".") -> Dict[str, Any]: Returns a list of all files and subdirectories in the target directory.

## Development & Testing

Run unit tests locally with uv:

uv sync
uv run pytest

## License

MIT