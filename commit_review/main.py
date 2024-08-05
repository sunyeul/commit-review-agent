import os
import sys

from git import Repo

from .api_manager import APIManager
from .file_review import process_and_review_files
from .git_utils import (
    get_staged_python_files,
)

# def commit_changes_if_confirmed(repo):
#     """コミットの実行確認と実行を行います。"""
#     if confirm_commit():
#         commit_message = repo.head.commit.message.strip()
#         if not commit_message:
#             commit_message = input("コミットメッセージを入力してください: ").strip()
#         if commit_message:
#             commit_changes(repo, commit_message)
#         else:
#             print("エラー: コミットメッセージが空です。コミットを中止します。")
#             exit(1)
#     else:
#         print("コミットがキャンセルされました。")
#         exit(1)


def main(review_point: str, api_choice: str) -> None:
    """メイン関数。ステージされたPythonファイルに対してレビューを行います。"""
    repo = Repo(os.getcwd(), search_parent_directories=True)
    os.chdir(repo.working_tree_dir)

    api_manager = APIManager(api_choice)

    files = get_staged_python_files(repo)
    if not files:
        print("エラー: 変更されたPythonファイルがありません")
        return

    commit_okay: bool = process_and_review_files(api_manager, files, repo, review_point)

    if commit_okay:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
