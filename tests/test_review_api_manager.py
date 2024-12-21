from unittest.mock import Mock, patch

import pytest

from commit_review.review_api_manager import ReviewAPIManager


@pytest.fixture
def review_manager():
    return ReviewAPIManager(api_choice="openai")


def test_get_model_openai(review_manager):
    with patch("commit_review.review_api_manager.ChatOpenAI") as mock_openai:
        review_manager.get_model()
        mock_openai.assert_called_once_with(model="gpt-4o", temperature=0.1)


def test_get_model_anthropic():
    manager = ReviewAPIManager(api_choice="anthropic")
    with patch("commit_review.review_api_manager.ChatAnthropic") as mock_anthropic:
        manager.get_model()
        mock_anthropic.assert_called_once_with(
            model="claude-3-5-sonnet-20240620", temperature=0.1
        )


def test_request_review(review_manager):
    mock_chain = Mock()
    mock_result = {"file_contents_explanation": "テスト説明", "is_commit_okay": True}

    # チェーンの設定
    mock_chain.invoke.return_value = mock_result

    # prompt_template | model | parser 全体をモック
    with patch("commit_review.review_api_manager.prompt_template") as mock_prompt:
        with patch("commit_review.review_api_manager.parser"):
            with patch.object(review_manager, "get_model"):
                # チェーンの構築をモック
                mock_prompt.__or__.return_value.__or__.return_value = mock_chain

                result = review_manager.request_review(
                    file_contents="test",
                    file_changes="test",
                    commit_message="test",
                    review_point=None,
                )

                assert result["is_commit_okay"] is True
                assert result["file_contents_explanation"] == "テスト説明"
