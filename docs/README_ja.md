# ft_transcendence

[English version](../README.md)

## 概要

ft_transcendenceは、42の最終課題として開発されたウェブアプリケーションプロジェクトです。このプロジェクトでは、Djangoをバックエンドに使用し、HTML、CSS、JavaScript、Bootstrapを用いてフロントエンドを構築しています。ソケット通信を利用して、リアルタイムのPingPongゲーム対戦やリアルタイムチャット機能を実現しています。

また、GrafanaとPrometheusをDockerで統合し、サーバーの状態をモニタリングすることができます。

## 主な機能

1. **PingPongゲーム**:

   - 2本のパドルと1つのボールを使用して得点を競うゲーム
   - リモートプレイ機能
   - トーナメントモード

2. **リアルタイムチャット**:

   - 個人間のプライベートチャット
   - リアルタイムでのメッセージ送受信
   - `:invite`コマンドを使用してチャット相手をゲームに招待可能

3. **サーバーモニタリング**:
   - GrafanaとPrometheusを使用したサーバー状態の可視化

## セットアップ手順

### 前提条件

- Dockerが動作する環境

### インストール

1. リポジトリをクローンします：

   ```sh
   git clone https://github.com/yuki-shimoda-crypto/42_ft_transcendence.git
   cd ft_transcendence
   ```

2. 環境変数ファイルをコピーします：

   ```sh
   cp .env.example .env
   ```

3. Dockerコンテナを起動します：
   ```sh
   sudo make up-d
   ```

これにより、以下のサービスがバックグラウンドで起動します：

- web-prod (製品デプロイ用)
- web-dev (開発環境)
- web-db (データベース)
- grafana
- prometheus

### アクセス方法

- ウェブアプリケーション: `https://localhost:8000`
- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`

注：GrafanaとPrometheusの詳細な設定と使用方法については、[MONITOR_README.md](./MONITOR_README.md)を参照してください。

## 開発環境

開発環境でプロジェクトを実行するには：

1. 開発用コンテナに入ります：

   ```sh
   sudo make exec web-dev
   ```

2. SSL証明書を生成します：

   ```sh
   CERT_PATH="./cert.pem"
   KEY_PATH="./key.pem"
   openssl req -x509 -newkey rsa:4096 -keyout "$KEY_PATH" -out "$CERT_PATH" -days 365 -nodes -subj "/CN=localhost"
   ```

3. 開発サーバーを起動します：

   ```sh
   daphne -e ssl:8000:privateKey=key.pem:certKey=cert.pem PongChat.asgi:application
   ```

4. `https://localhost:8001`にアクセスして開発を行います。

注意：ファイルを変更した場合は、サーバーを再起動して変更を反映させてください。

## ディレクトリ構造

```txt
.
├── PongChat
│   ├── PongChat
│   ├── accounts
│   ├── chat
│   ├── locale
│   ├── media
│   ├── pingpong
│   ├── static
│   └── templates
├── data
├── docs
├── node_modules
├── sample_code
├── tests
└── tools
    └── docker
        ├── web_dev
        └── web_prod
```

## 使用技術

- Backend: Django 5.0.4
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Database: PostgreSQL
- Real-time Communication: Django Channels
- Containerization: Docker
- Monitoring: Grafana, Prometheus

その他の依存関係については[requirements.txt](../requirements.txt)を参照してください。

## コントリビューション

問題や提案がある場合は、Issueを作成してください。

## コントリビューター

<a href="https://github.com/yuki-shimoda-crypto/42_ft_transcendence/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuki-shimoda-crypto/42_ft_transcendence" />
</a>

## ライセンス

このプロジェクトは[MIT License](../LICENSE)の下で公開されています。

## 連絡先

現在、特定の連絡先情報はありません。質問や懸念がある場合は、GitHubのIssueを通じてお問い合わせください。
