#!/usr/bin/env python3
import sys
import json
from PIL import Image

def crop_and_join_images(image_path, json_path, output_path="output.png"):
    """
    指定されたJSONファイルの座標情報に基づいて画像を切り取り、
    それらを水平に連結して新しい画像として保存する。

    Parameters:
    - image_path: 元画像のファイルパス
    - json_path: 座標情報を含むJSONファイルのパス
    - output_path: 出力画像のファイルパス（デフォルトは'output.png'）
    """
    try:
        # 画像を開く
        original_image = Image.open(image_path)

        # JSONファイルを読み込む
        with open(json_path, 'r') as f:
            crop_data = json.load(f)

        # 切り取った画像を格納するリスト
        cropped_images = []

        # 各座標情報に基づいて画像を切り取る
        for item in crop_data:
            x = item.get('x', 0)
            y = item.get('y', 0)
            width = item.get('width', 0)
            height = item.get('height', 0)

            # 座標情報が有効であることを確認
            if width <= 0 or height <= 0:
                print(f"警告: 無効な切り抜き領域: {item}")
                continue

            # 画像を切り取る
            cropped_image = original_image.crop((x, y, x + width, y + height))
            cropped_images.append(cropped_image)

        if not cropped_images:
            print("エラー: 有効な切り抜き領域がありません。")
            return False

        # 全ての切り取った画像の高さを確認
        heights = [img.height for img in cropped_images]
        max_height = max(heights)

        # 全ての切り取った画像の幅を合計
        total_width = sum(img.width for img in cropped_images)

        # 新しい画像を作成（水平連結用）
        result_image = Image.new('RGBA', (total_width, max_height))

        # 切り取った画像を水平に連結
        current_x = 0
        for img in cropped_images:
            # 画像を貼り付ける
            result_image.paste(img, (current_x, 0))
            current_x += img.width

        # 結果を保存
        result_image.save(output_path)
        print(f"出力画像を保存しました: {output_path}")
        return True

    except FileNotFoundError as e:
        print(f"エラー: ファイルが見つかりません: {e}")
        return False
    except json.JSONDecodeError:
        print(f"エラー: JSONファイルの形式が無効です: {json_path}")
        return False
    except Exception as e:
        print(f"エラー: {e}")
        return False

def main():
    # コマンドライン引数の解析
    if len(sys.argv) < 3:
        print("使用方法: python script.py <画像ファイル> <JSONファイル> [出力ファイル]")
        return

    image_path = sys.argv[1]
    json_path = sys.argv[2]

    # 出力ファイル名が指定されている場合は使用する
    output_path = "output.png"
    if len(sys.argv) > 3:
        output_path = sys.argv[3]

    # 画像の切り取りと連結を実行
    crop_and_join_images(image_path, json_path, output_path)

if __name__ == "__main__":
    main()
