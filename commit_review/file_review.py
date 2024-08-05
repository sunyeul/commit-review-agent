from .api_manager import APIManager
from .git_utils import get_changed_content, get_file_content
from .json_parser import extract_and_parse_json


def get_review_for_file(api_manager: APIManager, file, repo, review_point):
    """
    特定のファイルに対するレビューをリクエストし、結果を返します。

    Parameters:
    - api_manager (APIManager): APIManagerインスタンス
    - file (str): レビュー対象のファイルパス
    - repo (git.Repo): Gitリポジトリオブジェクト
    - review_point (str): レビューポイント

    Returns:
    - str: レビューテキスト
    """
    # ファイルの完全な内容を取得
    full_content = get_file_content(file)
    # 変更された内容を取得
    changed_content = get_changed_content(repo, file)

    if not changed_content:
        print(f"エラー: {file} ファイルの変更された内容がありません。")
        return None

    # APIマネージャーを使用してレビューをリクエスト
    review_result = api_manager.request_review(
        full_content, changed_content, review_point
    )

    return extract_and_parse_json(review_result)


def process_and_review_files(api_manager: APIManager, files, repo, review_point):
    """
    複数のファイルに対するレビューを処理します。

    Parameters:
    - api_manager (APIManager): APIManagerインスタンス
    - files (list): レビュー対象のファイルのリスト
    - repo (git.Repo): Gitリポジトリオブジェクト
    - review_point (str): レビューポイント
    """
    review_results = []
    for file in files:
        # ファイルに対するレビューを取得
        review_result = get_review_for_file(api_manager, file, repo, review_point)
        if review_result:
            print(
                f"{api_manager.api_choice.capitalize()}の {file} ファイルに対するレビュー:"
            )
            print(review_result)
            review_results.append(review_result.get("commit", False))
        else:
            print(f"エラー: {file} ファイルに対するレビューを取得できませんでした。")
    return all(review_results)
