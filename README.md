# コミットレビュエージェント (commit-review-agent)

`commit-review-agent`は、Gitのコミット前にPythonファイルのコードレビューを自動化するためのパッケージです。OpenAIのGPT-4o-miniやAnthropicのClaudeを利用して、コードの変更箇所をレビューします。

## インストール

以下の手順に従って、`commit-review-agent`パッケージをインストールしてください。

```bash
pip install git+https://github.com/yourusername/commit-review-agent.git
```

## 使用方法

`commit-review-agent`パッケージは、コマンドラインツールとして使用できます。以下のコマンドを実行して、ステージされたPythonファイルのコードレビューを行います。

```bash
commit-review-agent
```

## 開発

## pre-commitとの連携

pre-commitフックを設定して、コミット前にコードを自動的にレビューします。以下の手順に従って設定してください。

1. pre-commit-config.yamlファイルを作成

    ```yaml
    -   repo: https://github.com/sunyeul/commit-review-agent
        hooks:
        - id: commie-review
            name: Commit Review
            entry: commit-review-agent
            language: python
            types: [python]
            pass_filenames: false
            verbose: true
    ```

2. pre-commitをインストールして有効化

    ```bash
    pip install pre-commit
    pre-commit install
    ```

これで、Gitのコミット前に自動的にコードレビューが実行されるようになります。

## 環境変数の設定

コードレビューを行うために、OpenAIおよびAnthropicのAPIキーを環境変数として設定する必要があります。プロジェクトのルートディレクトリに'.env'ファイルを作成し、以下の内容を追加します。

```env
CLAUDE_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
```

## ライセンス

このプロジェクトはMITライセンスのもとで公開されています。詳細については、LICENSEファイルを参照してください。

このREADME.mdファイルは、見やすさと可読性を向上させるために適切に整えられています。各セクションは明確に区切られ、コードブロックはインデントされています。
