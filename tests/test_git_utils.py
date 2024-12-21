from unittest.mock import Mock, patch

import pytest
from git import Repo

from commit_review.git_utils import (
    get_staged_file_changes,
    get_staged_file_contents,
    get_staged_python_files,
)


@pytest.fixture
def mock_repo():
    return Mock(spec=Repo)


def test_get_staged_python_files(mock_repo):
    mock_repo.git.diff.return_value = "file1.py\nfile2.txt\nfile3.py"
    result = get_staged_python_files(mock_repo)
    assert result == ["file1.py", "file3.py"]
    mock_repo.git.diff.assert_called_once_with("--cached", name_only=True)


@patch("builtins.open", create=True)
def test_get_staged_file_contents(mock_open, mock_repo):
    mock_file = Mock()
    mock_file.read.return_value = "テストファイルの内容"
    mock_open.return_value.__enter__.return_value = mock_file

    result = get_staged_file_contents(["test.py"])
    assert "テストファイルの内容" in result
    assert "test.py" in result

    mock_open.assert_called_once_with("test.py", "r", encoding="utf-8")
    mock_file.read.assert_called_once()


def test_get_staged_file_changes(mock_repo):
    mock_repo.git.diff.return_value = """
+新しい行
-削除された行
    """
    result = get_staged_file_changes(["test.py"], mock_repo)
    assert "+新しい行" in result
    assert "-削除された行" in result
