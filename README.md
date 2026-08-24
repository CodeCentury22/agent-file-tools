# Agent File Tools (`agent-file-tools`)

Cross-platform file manipulation tools for local AI agents, featuring POSIX path normalization, automatic directory creation, and integrated audit telemetry.

## Features

* **Cross-Platform POSIX Normalization:** Converts Windows backslashes (`\`) and relative paths to resolved POSIX strings (`/`) for seamless ChromaDB vector memory compatibility.
* **Integrated Telemetry & Audit Logs:** Decorates operations with `@track_latency` and `@audit_logger` from `agent-core-utils` to emit structured execution logs (`file_tools_telemetry.jsonl`).
* **Safe Write Controls:** Supports overwrite prevention and automatic parent directory creation (`mkdir -p`).

## Installation

Link locally via `uv` or add to `pyproject.toml`:

```toml
[dependencies]
agent-file-tools = { git = "https://github.com/CodeCentury22/agent-file-tools.git", tag = "v0.5.0" }
```

## Quickstart

```python
from agent_file_tools.tools import (
    read_file,
    write_file,
    delete_file,
    list_files,
)

# 1. Write File
result = write_file(
    "workspace/example.py",
    "print('Hello Agent')",
    overwrite=True,
)
print(result)
# Output:
# {
#     'file_path': '/path/to/workspace/example.py',
#     'bytes_written': 20,
#     'status': 'SUCCESS'
# }

# 2. Read File
data = read_file("workspace/example.py")
print(data["content"])
# Output: "print('Hello Agent')"

# 3. List Directory
files = list_files("workspace")
print(files["files"])
# Output: ['example.py']

# 4. Delete File
delete_file("workspace/example.py")
```

## API Reference

| Function                                                             | Parameters                            | Description                                                 |
| -------------------------------------------------------------------- | ------------------------------------- | ----------------------------------------------------------- |
| `read_file(file_path: str)`                                          | `file_path`                           | Reads text content using UTF-8 encoding.                    |
| `write_file(file_path: str, code_body: str, overwrite: bool = True)` | `file_path`, `code_body`, `overwrite` | Writes file content, creating parent directories as needed. |
| `delete_file(file_path: str)`                                        | `file_path`                           | Deletes the targeted file if it exists.                     |
| `list_files(directory: str = ".")`                                   | `directory`                           | Returns a list of file names inside the target directory.   |

## License

MIT
