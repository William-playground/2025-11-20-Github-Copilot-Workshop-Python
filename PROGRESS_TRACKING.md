# 配達進捗管理システム

日付ベースの進捗管理機能を実装したキッチン配達ゲームシステムです。

## 機能

### バックエンド (deliverManager.py)
- 日付ごとの配達進捗を記録
- 成功・失敗・合計の配達数を集計
- 今日の進捗を取得
- 特定の日付の進捗を取得

### Web API (app.py)
Flask を使用した REST API:
- `GET /api/progress/today` - 今日の進捗を取得
- `GET /api/progress/<date>` - 指定日付の進捗を取得
- `GET /api/progress/all` - すべての日付の進捗を取得
- `POST /api/deliver` - レシピ配達をテスト

### フロントエンド (templates/index.html)
- 今日の日付を表示
- 成功した配達数、失敗した配達数、合計配達数を表示
- 材料を選択してレシピ配達をテスト
- リアルタイムで進捗を更新

## セットアップ

### 依存関係のインストール
```bash
pip install -r requirements.txt
```

### サーバーの起動
```bash
python3 app.py
```

サーバーは `http://localhost:5000` で起動します。

## 使用方法

1. ブラウザで `http://localhost:5000` を開く
2. 材料を選択する (Bread, Lettuce, Tomato)
3. 「配達を実行」ボタンをクリック
4. 進捗統計がリアルタイムで更新されます

### レシピ
- **Sandwich**: Bread + Lettuce + Tomato
- **Salad**: Lettuce + Tomato

## テスト

### API テスト
```bash
# サーバーを起動してから別のターミナルで:
python3 test_api.py
```

### 基本機能テスト
```bash
python3 deliverManager.py
```

## アーキテクチャ

### データフロー
1. ユーザーが材料を選択してフロントエンドから配達リクエスト
2. Flask API が `/api/deliver` エンドポイントでリクエストを受信
3. DeliveryManager が配達を処理し、日付ごとの進捗を更新
4. API が結果と更新された進捗をフロントエンドに返送
5. フロントエンドが統計とメッセージを表示

### 日付ベースの進捗管理
- `defaultdict` を使用して日付ごとの進捗を管理
- ISO 8601 形式 (YYYY-MM-DD) で日付をキーとして使用
- 各日付に対して `{'successful': int, 'failed': int, 'total': int}` を記録
