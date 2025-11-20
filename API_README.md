# バックエンドAPI ドキュメント

## 概要
このAPIは、キッチンゲームの進捗データを管理するためのRESTful APIです。

## 起動方法

### 必要な依存関係のインストール
```bash
pip install -r requirements.txt
```

### APIサーバーの起動
```bash
python3 api_server.py
```

サーバーは `http://localhost:5000` で起動します。

**デバッグモード（開発環境のみ）:**
```bash
FLASK_DEBUG=true python3 api_server.py
```

**注意:** デバッグモードは開発時のみ使用してください。本番環境では絶対に使用しないでください。

## APIエンドポイント

### 1. ヘルスチェック
サーバーの稼働状態を確認します。

**エンドポイント:** `GET /health`

**レスポンス例:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-20T02:22:03.682Z"
}
```

### 2. 進捗データの取得
現在の進捗データを取得します。

**エンドポイント:** `GET /progress`

**レスポンス例:**
```json
{
  "status": "success",
  "data": {
    "successful_recipes_amount": 5,
    "waiting_recipes": [
      {"name": "Sandwich"},
      {"name": "Salad"}
    ],
    "last_updated": "2025-11-20T02:22:03.682Z"
  }
}
```

### 3. 進捗データの保存
進捗データを保存・更新します。

**エンドポイント:** `POST /progress`

**リクエストボディ:**
```json
{
  "successful_recipes_amount": 5,
  "waiting_recipes": [
    {"name": "Sandwich"},
    {"name": "Salad"}
  ]
}
```

**レスポンス例:**
```json
{
  "status": "success",
  "message": "進捗データが保存されました",
  "data": {
    "successful_recipes_amount": 5,
    "waiting_recipes": [
      {"name": "Sandwich"},
      {"name": "Salad"}
    ],
    "last_updated": "2025-11-20T02:22:03.682Z"
  }
}
```

### 4. 進捗データのリセット
進捗データを初期状態にリセットします。

**エンドポイント:** `POST /progress/reset`

**レスポンス例:**
```json
{
  "status": "success",
  "message": "進捗データがリセットされました",
  "data": {
    "successful_recipes_amount": 0,
    "waiting_recipes": [],
    "last_updated": "2025-11-20T02:22:03.682Z"
  }
}
```

## データ管理

現在の実装では、進捗データは**メモリ内**に保存されます。サーバーを再起動すると、データは失われます。

将来的には以下のような永続化オプションを検討できます：
- ファイルベース（JSON、CSVなど）
- SQLiteデータベース
- PostgreSQL、MySQLなどのRDBMS
- RedisなどのNoSQLデータベース

## 使用例

### curlを使用した例

```bash
# ヘルスチェック
curl -X GET http://localhost:5000/health

# 進捗データの取得
curl -X GET http://localhost:5000/progress

# 進捗データの保存
curl -X POST http://localhost:5000/progress \
  -H "Content-Type: application/json" \
  -d '{"successful_recipes_amount": 10, "waiting_recipes": [{"name": "Pizza"}]}'

# 進捗データのリセット
curl -X POST http://localhost:5000/progress/reset
```

### Pythonクライアントを使用した例

`api_client_demo.py`を実行してください：

```bash
python3 api_client_demo.py
```

このデモでは、ゲームシミュレーションを実行し、APIを使用して進捗データを保存・取得します。

## セキュリティに関する注意

本実装は開発・学習目的のものです。本番環境で使用する場合は、以下の対策を検討してください：

- 認証・認可の実装
- HTTPS/TLSの使用
- レート制限の実装
- 入力バリデーションの強化
- SQLインジェクション対策（データベース使用時）
- CORS設定の見直し
