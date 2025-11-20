#!/usr/bin/env python3
"""
API エンドポイントのテストスクリプト
"""
import requests
import time
from datetime import date

# Flask サーバーのベースURL
BASE_URL = "http://localhost:5000"


def test_today_progress():
    """今日の進捗取得APIのテスト"""
    print("=== 今日の進捗取得APIテスト ===")
    response = requests.get(f"{BASE_URL}/api/progress/today")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ ステータス: {response.status_code}")
        print(f"📅 日付: {data['date']}")
        print(f"📊 進捗: {data['progress']}")
        return True
    else:
        print(f"❌ エラー: {response.status_code}")
        return False


def test_deliver_success():
    """成功する配達のテスト (Sandwich: Bread + Lettuce + Tomato)"""
    print("\n=== 成功する配達テスト (Sandwich) ===")
    response = requests.post(
        f"{BASE_URL}/api/deliver",
        json={"ingredients": [3, 2, 1]}  # Bread, Lettuce, Tomato
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ ステータス: {response.status_code}")
        print(f"🎉 結果: {data['message']}")
        print(f"✅ 成功: {data['success']}")
        print(f"📊 今日の進捗: {data['today_progress']}")
        return data['success']
    else:
        print(f"❌ エラー: {response.status_code}")
        return False


def test_deliver_fail():
    """失敗する配達のテスト (存在しないレシピ)"""
    print("\n=== 失敗する配達テスト (Invalid Recipe) ===")
    response = requests.post(
        f"{BASE_URL}/api/deliver",
        json={"ingredients": [3]}  # Bread only
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ ステータス: {response.status_code}")
        print(f"📝 結果: {data['message']}")
        print(f"❌ 成功: {data['success']}")
        print(f"📊 今日の進捗: {data['today_progress']}")
        return not data['success']  # 失敗を期待
    else:
        print(f"❌ エラー: {response.status_code}")
        return False


def test_progress_by_date():
    """特定の日付の進捗取得APIのテスト"""
    print("\n=== 特定日付の進捗取得APIテスト ===")
    today = date.today().isoformat()
    response = requests.get(f"{BASE_URL}/api/progress/{today}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ ステータス: {response.status_code}")
        print(f"📅 日付: {data['date']}")
        print(f"📊 進捗: {data['progress']}")
        return True
    else:
        print(f"❌ エラー: {response.status_code}")
        return False


def test_all_progress():
    """全ての進捗取得APIのテスト"""
    print("\n=== 全進捗取得APIテスト ===")
    response = requests.get(f"{BASE_URL}/api/progress/all")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ ステータス: {response.status_code}")
        print(f"📊 全進捗データ: {data['progress']}")
        return True
    else:
        print(f"❌ エラー: {response.status_code}")
        return False


def run_all_tests():
    """全てのテストを実行"""
    print("🧪 APIテストを開始します...\n")
    
    results = []
    
    # サーバーが起動するまで少し待つ
    print("⏳ サーバーの起動を待っています...")
    time.sleep(2)
    
    try:
        results.append(("今日の進捗取得", test_today_progress()))
        results.append(("成功する配達", test_deliver_success()))
        results.append(("失敗する配達", test_deliver_fail()))
        results.append(("特定日付の進捗取得", test_progress_by_date()))
        results.append(("全進捗取得", test_all_progress()))
        
        print("\n" + "="*50)
        print("📊 テスト結果サマリー")
        print("="*50)
        
        passed = 0
        failed = 0
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
            if result:
                passed += 1
            else:
                failed += 1
        
        print("="*50)
        print(f"合計: {len(results)} テスト | 成功: {passed} | 失敗: {failed}")
        
        if failed == 0:
            print("\n🎉 全てのテストが成功しました！")
            return 0
        else:
            print(f"\n⚠️  {failed}個のテストが失敗しました")
            return 1
            
    except requests.exceptions.ConnectionError:
        print("\n❌ エラー: サーバーに接続できません")
        print("app.py が実行されているか確認してください")
        return 1


if __name__ == "__main__":
    exit(run_all_tests())
