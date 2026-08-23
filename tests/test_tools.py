import pytest
from pathlib import Path
from agent_file_tools.tools import read_file, write_file, delete_file, list_files


def test_write_and_read_file(tmp_path):
    test_file = str(tmp_path / "sample.py")
    content = "print('Hello Agent')"

    write_res = write_file(test_file, content)
    assert write_res["status"] == "SUCCESS"
    assert write_res["bytes_written"] > 0
    # POSIX path assertion
    assert write_res["file_path"] == Path(test_file).resolve().as_posix()

    read_res = read_file(test_file)
    assert read_res["status"] == "SUCCESS"
    assert read_res["content"] == content


def test_write_file_no_overwrite(tmp_path):
    test_file = str(tmp_path / "existing.txt")
    write_file(test_file, "Initial content")

    res = write_file(test_file, "New Content", overwrite=False)
    assert res["status"] == "DENIED"
    assert "overwrite" in res["error"]


def test_delete_file(tmp_path):
    test_file = str(tmp_path / "temp.txt")
    write_file(test_file, "To be deleted")

    del_res = delete_file(test_file)
    assert del_res["status"] == "SUCCESS"
    assert not Path(test_file).exists()


def test_list_files(tmp_path):
    write_file(str(tmp_path / "a.txt"), "A")
    write_file(str(tmp_path / "b.txt"), "B")

    res = list_files(str(tmp_path))
    assert res["status"] == "SUCCESS"
    assert "a.txt" in res["files"]
    assert "b.txt" in res["files"]