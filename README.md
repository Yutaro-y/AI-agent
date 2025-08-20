# Agent Lang Stream MCP

このプロジェクトは、Streamlitを使用してインタラクティブなチャットアプリケーションを構築するものです。OpenAIのAPIを利用して、ユーザーの入力に基づいた応答を生成します。

## 機能

- OpenAIのGPT-4モデルを使用したチャットボット
- ユーザーとのメッセージ履歴の管理
- MCP（Multi-Client Protocol）を使用したツールの管理

## 必要な環境

- Python 3.x
- 必要なパッケージは`requirements.txt`に記載されています。

## セットアップ

1. リポジトリをクローンします。
   ```bash
   git clone <repository-url>
   cd agent-lang-stream-mcp
   ```

2. 環境変数ファイルを作成し、OpenAI APIキーを設定します。
   ```bash
   echo "OPENAI_API_KEY=your_api_key" > .env
   ```

3. 必要なパッケージをインストールします。
   ```bash
   pip install -r requirements.txt
   ```

4. アプリケーションを実行します。
   ```bash
   streamlit run streamlit_app2.py
   ```

## 使用方法

アプリケーションを起動すると、チャットインターフェースが表示されます。ユーザーは入力ボックスにメッセージを入力し、送信することでチャットボットと対話できます。ボットはMCPを使用してツールを呼び出し、応答を生成します。

## 注意事項

- 環境変数ファイル（`.env`）には、機密情報を含めないでください。
- アプリケーションの実行には、インターネット接続が必要です。
