import os
import sys
from typing import Optional

from git import Repo

from .git_utils import (
    get_commit_message,
    get_staged_file_changes,
    get_staged_file_contents,
    get_staged_python_files,
)
from .review_api_manager import ReviewAPIManager


def main(api_choice: str, review_point: Optional[str] = None) -> None:
    """メイン関数。ステージされたPythonファイルに対してレビューを行います。"""
    repo = Repo(os.getcwd(), search_parent_directories=True)
    os.chdir(repo.working_tree_dir)

    review_api_manager = ReviewAPIManager(api_choice=api_choice)

    staged_python_files = get_staged_python_files(repo=repo)
    print("staged_python_files", staged_python_files)
    if not staged_python_files:
        print("変更されたPythonファイルがありません")
        sys.exit(0)

    staged_file_contents = get_staged_file_contents(file_paths=staged_python_files)
    staged_file_changes = get_staged_file_changes(
        file_paths=staged_python_files, repo=repo
    )
    commit_message = get_commit_message(repo=repo)

    result = review_api_manager.request_review(
        file_contents=staged_file_contents,
        file_changes=staged_file_changes,
        commit_message=commit_message,
        review_point=review_point,
    )

    is_commit_okay = result["is_commit_okay"]
    print("\nコミットレビュー結果:\n")
    print(f"コミットメッセージ: {commit_message}\n")
    print(f"コードの説明: {result['file_contents_explanation']}\n")
    print(f"変更点の説明: {result['file_changes_explanation']}\n")
    print(
        f"コミットメッセージのレビュー結果: {result['commit_message_review_result']}\n"
    )
    print(f"コミット内容のレビュー結果: {result['commit_content_review_result']}\n")
    print(f"コミットレビューの総合結果: {result['commit_review_result']}\n")
    print("改善点のリスト:\n")
    for improvement in result["suggested_improvements"]:
        print(f"  - {improvement}\n")
    print(f"コミット可否: {'Okay' if result['is_commit_okay'] else 'Not Okay'}\n")

    if is_commit_okay:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
