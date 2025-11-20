"""
シンプルなFlask APIバックエンド
日付ごとの進捗を取得・表示する
"""
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from deliverManager import (
    DeliveryManager, RecipeListSO, RecipeSO, KitchenObjectSO,
    PlateKitchenObject, KitchenGameManager
)
from datetime import date

app = Flask(__name__)
CORS(app)  # フロントエンドからのアクセスを許可

# サンプルデータでDeliveryManagerを初期化
tomato = KitchenObjectSO("Tomato", 1)
lettuce = KitchenObjectSO("Lettuce", 2)
bread = KitchenObjectSO("Bread", 3)

sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
salad_recipe = RecipeSO("Salad", [lettuce, tomato])

recipe_list = RecipeListSO([sandwich_recipe, salad_recipe])

# ゲームマネージャーとデリバリーマネージャーを初期化
game_manager = KitchenGameManager.get_instance()
game_manager.start_game()

delivery_manager = DeliveryManager.get_instance(recipe_list)


@app.route('/')
def index():
    """フロントエンドのHTMLページを表示"""
    return render_template('index.html')


@app.route('/api/progress/today', methods=['GET'])
def get_today_progress():
    """今日の進捗を取得するAPIエンドポイント"""
    progress = delivery_manager.get_today_progress()
    return jsonify({
        'date': date.today().isoformat(),
        'progress': progress
    })


@app.route('/api/progress/<date_str>', methods=['GET'])
def get_progress_by_date(date_str):
    """指定した日付の進捗を取得するAPIエンドポイント
    
    Args:
        date_str: 日付文字列 (YYYY-MM-DD形式)
    """
    try:
        # 日付の妥当性チェック
        date.fromisoformat(date_str)
        progress = delivery_manager.get_progress_by_date(date_str)
        return jsonify({
            'date': date_str,
            'progress': progress
        })
    except ValueError:
        return jsonify({'error': '無効な日付形式です。YYYY-MM-DD形式で指定してください。'}), 400


@app.route('/api/progress/all', methods=['GET'])
def get_all_progress():
    """全ての日付の進捗を取得するAPIエンドポイント"""
    all_progress = delivery_manager.get_all_daily_progress()
    return jsonify({
        'progress': all_progress
    })


@app.route('/api/deliver', methods=['POST'])
def deliver_recipe():
    """レシピ配達をシミュレートするAPIエンドポイント
    
    Request Body:
        {
            "ingredients": [1, 2, 3]  // KitchenObjectSOのIDリスト
        }
    """
    data = request.json
    ingredient_ids = data.get('ingredients', [])
    
    # レシピを生成するために少しupdateを実行
    # (実際のゲームではバックグラウンドで常にupdateが呼ばれるが、
    #  APIテストのために明示的に呼び出す)
    import time
    if len(delivery_manager.get_waiting_recipe_so_list()) == 0:
        start = time.time()
        while time.time() - start < 5 and len(delivery_manager.get_waiting_recipe_so_list()) < 2:
            delivery_manager.update()
            time.sleep(0.1)
    
    # PlateKitchenObjectを作成
    plate = PlateKitchenObject()
    
    # 利用可能な材料マッピング
    available_ingredients = {
        1: tomato,
        2: lettuce,
        3: bread
    }
    
    for ingredient_id in ingredient_ids:
        if ingredient_id in available_ingredients:
            plate.add_kitchen_object(available_ingredients[ingredient_id])
    
    # 配達を試みる
    initial_success_count = delivery_manager.get_successful_recipes_amount()
    delivery_manager.deliver_recipe(plate)
    final_success_count = delivery_manager.get_successful_recipes_amount()
    
    success = final_success_count > initial_success_count
    
    return jsonify({
        'success': success,
        'message': 'レシピ配達成功！' if success else 'レシピ配達失敗...',
        'total_successful': final_success_count,
        'today_progress': delivery_manager.get_today_progress()
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
