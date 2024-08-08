import os
from typing import List

from git import GitCommandError, Repo


def get_staged_python_files(repo: Repo) -> List[str]:
    """ステージされたPythonファイルのリストを取得します。"""
    try:
        diff = repo.git.diff("--cached", name_only=True)
        return [item for item in diff.splitlines() if item.endswith(".py")]
    except GitCommandError as e:
        print(f"エラー: Gitコマンドの実行中にエラーが発生しました: {e}")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
    return []


def get_file_content(file_path: str) -> str:
    """指定されたファイルの内容を取得します。"""
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        raise FileNotFoundError(f"エラー: {file_path} ファイルが存在しないか空です")
    with open(file_path, "r") as f:
        return f.read()


def get_changed_content(repo: Repo, file_path: str) -> str:
    """ステージされたファイルの変更された内容を取得します。"""
    try:
        diff = repo.git.diff("--cached", file_path, unified=0)
        return "\n".join(
            [
                line
                for line in diff.splitlines()
                if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))
            ]
        )
    except GitCommandError as e:
        print(f"エラー: Gitコマンドの実行中にエラーが発生しました: {e}")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
    return ""
