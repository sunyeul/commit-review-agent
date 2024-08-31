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


def get_staged_file_contents(file_paths: List[str]) -> str:
    """ステージされたファイルの内容を取得します。"""
    try:
        staged_file_contents = ""

        for file_path in file_paths:
            if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
                continue
            with open(file_path, "r") as f:
                staged_file_contents += f"----------{file_path}----------\n"
                staged_file_contents += f.read()
                staged_file_contents += "\n" + "-" * 40
        return staged_file_contents
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
    return ""


def get_staged_file_changes(file_paths: List[str], repo: Repo) -> str:
    """ステージされたファイルの変更された内容を取得します。"""
    try:
        staged_file_changes = ""

        for file_path in file_paths:
            diff = repo.git.diff("--cached", file_path, unified=0)
            staged_file_changes += f"----------{file_path}----------\n"
            staged_file_changes += "\n".join(
                [
                    line
                    for line in diff.splitlines()
                    if line.startswith(("+", "-"))
                    and not line.startswith(("+++", "---"))
                ]
            )
            staged_file_changes += "\n" + "-" * 40
        return staged_file_changes
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
    return ""


def get_commit_message(repo: Repo) -> str:
    """コミットメッセージを取得します。"""
    try:
        commit_msg_filepath = os.path.join(repo.git_dir, "COMMIT_EDITMSG")
        with open(commit_msg_filepath, "r") as file:
            commit_msg = file.read().strip()
        return commit_msg
    except FileNotFoundError:
        print(f"エラー: {commit_msg_filepath} ファイルが見つかりません")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
    return ""
