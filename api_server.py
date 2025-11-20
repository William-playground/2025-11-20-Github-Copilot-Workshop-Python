from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, List, Any
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# デバッグモードは環境変数で制御（デフォルトはFalse）
DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# In-memory data storage for progress data
progress_data: Dict[str, Any] = {
    "successful_recipes_amount": 0,
    "waiting_recipes": [],
    "last_updated": None
}


@app.route('/progress', methods=['GET'])
def get_progress():
    """
    進捗データを取得するエンドポイント
    Returns:
        JSON: 現在の進捗データ
    """
    return jsonify({
        "status": "success",
        "data": progress_data
    }), 200


@app.route('/progress', methods=['POST'])
def save_progress():
    """
    進捗データを保存するエンドポイント
    Request Body:
        {
            "successful_recipes_amount": int,
            "waiting_recipes": list (optional)
        }
    Returns:
        JSON: 保存結果
    """
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({
                "status": "error",
                "message": "リクエストボディが空です"
            }), 400
        
        # 成功したレシピ数を更新
        if "successful_recipes_amount" in data:
            progress_data["successful_recipes_amount"] = data["successful_recipes_amount"]
        
        # 待機中のレシピを更新（オプション）
        if "waiting_recipes" in data:
            progress_data["waiting_recipes"] = data["waiting_recipes"]
        
        # 最終更新時刻を記録
        progress_data["last_updated"] = datetime.now().isoformat()
        
        return jsonify({
            "status": "success",
            "message": "進捗データが保存されました",
            "data": progress_data
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"エラーが発生しました: {str(e)}"
        }), 500


@app.route('/progress/reset', methods=['POST'])
def reset_progress():
    """
    進捗データをリセットするエンドポイント
    Returns:
        JSON: リセット結果
    """
    global progress_data
    progress_data = {
        "successful_recipes_amount": 0,
        "waiting_recipes": [],
        "last_updated": datetime.now().isoformat()
    }
    
    return jsonify({
        "status": "success",
        "message": "進捗データがリセットされました",
        "data": progress_data
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """
    ヘルスチェックエンドポイント
    Returns:
        JSON: サーバーの状態
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    print("バックエンドAPIサーバーを起動中...")
    print("利用可能なエンドポイント:")
    print("  GET  /progress        - 進捗データの取得")
    print("  POST /progress        - 進捗データの保存")
    print("  POST /progress/reset  - 進捗データのリセット")
    print("  GET  /health          - ヘルスチェック")
    print(f"デバッグモード: {DEBUG_MODE}")
    app.run(host='0.0.0.0', port=5000, debug=DEBUG_MODE)
