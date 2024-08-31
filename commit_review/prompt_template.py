from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field


class ReviewResult(BaseModel):
    file_contents_explanation: str = Field(description="コードの説明")
    file_changes_explanation: str = Field(description="変更点の説明")
    commit_message_review_result: str = Field(
        description="コミットメッセージのレビュー結果"
    )
    commit_content_review_result: str = Field(description="コミット内容のレビュー結果")
    commit_review_result: str = Field(description="コミットレビューの総合結果")
    suggested_improvements: list[str] = Field(description="改善点のリスト")
    is_commit_okay: bool = Field(
        description="レビューの結果、commitしても問題なければTrue, それ以外はFalse"
    )


parser = JsonOutputParser(pydantic_object=ReviewResult)

prompt_template = PromptTemplate(
    template="""
あなたはコードレビュー担当者です。次の手順でコミットのレビューを行なってください。
1. コミットメッセージに変更目的と変更点が明記されているか
2. コミット内容がコミットメッセージと合致しているか

全ファイル内容:\n{file_contents}\n\n
変更された内容:\n{file_changes}\n\n
コミットメッセージ:\n{commit_message}\n\n
レビューポイント(Optional):\n{review_point}\n\n

結果:\n{format_instructions}

**必ず日本語に出力してください。**
""",
    input_variables=[
        "file_contents",
        "file_changes",
        "commit_message",
        "review_point",
    ],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
