import requests
import time
from deliverManager import (
    DeliveryManager, KitchenGameManager, KitchenObjectSO,
    RecipeSO, RecipeListSO, PlateKitchenObject
)

# APIサーバーのベースURL
API_BASE_URL = "http://127.0.0.1:5000"


def get_progress():
    """APIから進捗データを取得"""
    try:
        response = requests.get(f"{API_BASE_URL}/progress")
        if response.status_code == 200:
            return response.json()["data"]
        else:
            print(f"エラー: {response.status_code}")
            return None
    except Exception as e:
        print(f"API接続エラー: {e}")
        return None


def save_progress(successful_recipes_amount, waiting_recipes=None):
    """APIに進捗データを保存"""
    try:
        data = {
            "successful_recipes_amount": successful_recipes_amount
        }
        if waiting_recipes is not None:
            data["waiting_recipes"] = waiting_recipes
        
        response = requests.post(
            f"{API_BASE_URL}/progress",
            json=data
        )
        if response.status_code == 200:
            print("進捗データが保存されました")
            return response.json()
        else:
            print(f"保存エラー: {response.status_code}")
            return None
    except Exception as e:
        print(f"API接続エラー: {e}")
        return None


def reset_progress():
    """進捗データをリセット"""
    try:
        response = requests.post(f"{API_BASE_URL}/progress/reset")
        if response.status_code == 200:
            print("進捗データがリセットされました")
            return response.json()
        else:
            print(f"リセットエラー: {response.status_code}")
            return None
    except Exception as e:
        print(f"API接続エラー: {e}")
        return None


if __name__ == "__main__":
    print("=== バックエンドAPI統合デモ ===\n")
    
    # 1. 現在の進捗を取得
    print("1. 現在の進捗データを取得:")
    progress = get_progress()
    if progress:
        print(f"   成功したレシピ数: {progress['successful_recipes_amount']}")
        print(f"   待機中のレシピ数: {len(progress['waiting_recipes'])}")
        print(f"   最終更新: {progress['last_updated']}\n")
    
    # 2. 進捗をリセット
    print("2. 進捗データをリセット:")
    reset_progress()
    print()
    
    # 3. ゲームシミュレーション
    print("3. ゲームシミュレーション開始:")
    
    # サンプルデータ作成
    tomato = KitchenObjectSO("Tomato", 1)
    lettuce = KitchenObjectSO("Lettuce", 2)
    bread = KitchenObjectSO("Bread", 3)
    
    # サンプルレシピ
    sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
    salad_recipe = RecipeSO("Salad", [lettuce, tomato])
    
    recipe_list = RecipeListSO([sandwich_recipe, salad_recipe])
    
    # ゲームマネージャーとデリバリーマネージャーを初期化
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    
    delivery_manager = DeliveryManager.get_instance(recipe_list)
    
    # イベントハンドラー: レシピ成功時にAPIに保存
    def on_recipe_success(sender, args):
        print("   ✓ レシピ配達成功！")
        # APIに進捗を保存
        waiting_recipes = [
            {"name": recipe.name} 
            for recipe in delivery_manager.get_waiting_recipe_so_list()
        ]
        save_progress(
            delivery_manager.get_successful_recipes_amount(),
            waiting_recipes
        )
    
    delivery_manager.on_recipe_success.add_handler(on_recipe_success)
    
    # 5秒間ゲームを実行してレシピを生成
    print("   レシピを生成中...")
    start_time = time.time()
    while time.time() - start_time < 5:
        delivery_manager.update()
        time.sleep(0.1)
    
    # サンプル配達テスト
    print(f"   待機中のレシピ数: {len(delivery_manager.get_waiting_recipe_so_list())}")
    
    # サンドイッチを配達
    plate = PlateKitchenObject()
    plate.add_kitchen_object(bread)
    plate.add_kitchen_object(lettuce)
    plate.add_kitchen_object(tomato)
    
    print("   サンドイッチを配達...")
    delivery_manager.deliver_recipe(plate)
    
    # 4. 最終的な進捗を取得して表示
    print("\n4. 最終的な進捗データを取得:")
    final_progress = get_progress()
    if final_progress:
        print(f"   成功したレシピ数: {final_progress['successful_recipes_amount']}")
        print(f"   待機中のレシピ数: {len(final_progress['waiting_recipes'])}")
        print(f"   最終更新: {final_progress['last_updated']}")
    
    print("\n=== デモ完了 ===")
