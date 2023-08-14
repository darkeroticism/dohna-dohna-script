import glob
import imghdr
import math
import os

import cv2
import numpy as np

# 位置調整したい画像を保存しているフォルダを指定
INPUT_DIRECTORY_NAME: str = "input"

# ダウンロード画像の保存先フォルダを作成
OUTPUT_DIRECTORY_NAME: str = "output"

# カスケード型分類器のファイルパス
CASCADE_CLASSIFIER_FILE_NAME: str = "lbpcascade_animeface.xml"

# 自作ジンザイの画像サイズの規格は1024x1024
IMAGE_SPEC: int = 1024


def resize_square(img, size):
    """Resize the image to a square shape.

    Args:
        img (ndarray): input image.
        size (int): size of output(px).
    Returns:
        ndarray: resized image.
    """
    height, width = img.shape[:2]
    scale = size / max(width, height)
    target_width = math.floor(width * scale)
    target_height = math.floor(height * scale)

    if scale > 1:
        interpolation = cv2.INTER_LINEAR
    else:
        interpolation = cv2.INTER_AREA
    resized_image = cv2.resize(img, (target_width, target_height), interpolation=interpolation)

    zeros = np.zeros((size, size), dtype="uint8")

    channel = len(img.shape)
    if channel == 2:
        # 入力画像がグレースケールの時
        dst = cv2.merge([zeros])
    else:
        is_alpha = img.shape[2] == 4
        if is_alpha:
            # 入力画像がアルファチャンネルを持つカラー画像の時
            dst = cv2.merge([zeros, zeros, zeros, zeros])
        else:
            # 入力画像がアルファチャンネルを持たないカラー画像の時
            dst = cv2.merge([zeros, zeros, zeros])

    x_offset = size // 2 - target_width // 2
    y_offset = size // 2 - target_height // 2

    dst[y_offset : y_offset + target_height, x_offset : x_offset + target_width] = resized_image

    return dst


def main():
    try:
        os.mkdir(OUTPUT_DIRECTORY_NAME)
    except FileExistsError:
        pass

    # 画像ファイルのパスを配列に保存
    img_paths = [
        path
        for path in glob.glob(f"{INPUT_DIRECTORY_NAME}/**/*.*", recursive=True)
        if os.path.isfile(path) and imghdr.what(path)
    ]

    # 分類器の読み込み
    classifier = cv2.CascadeClassifier(CASCADE_CLASSIFIER_FILE_NAME)

    for img_path in img_paths:
        # 保存パスを作成
        file_name = os.path.splitext(os.path.basename(img_path))[0]
        save_path = f"{OUTPUT_DIRECTORY_NAME}/{file_name}_adjustment.png"

        # 画像を読み込み
        target_image = cv2.imread(img_path, flags=cv2.IMREAD_UNCHANGED)
        # 1024*1024にリサイズする
        resized_image = resize_square(target_image, IMAGE_SPEC)

        # 処理の高速化のためグレースケールに変換
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        # 顔の検出
        faces = classifier.detectMultiScale(gray_image)

        if len(faces):
            # 顔が検出出来たらイイ感じの位置に来るよう平行移動する
            x, y, w, h = faces[0]
            scale = 120 / w
            M = np.array(
                [
                    [scale, 0, -math.floor(x * scale) + 512 - math.floor(w * scale) // 2],
                    [0, scale, -math.floor(y * scale) + 150],
                ],
                dtype=np.float32,
            )
            dst = cv2.warpAffine(resized_image, M, (IMAGE_SPEC, IMAGE_SPEC))
            # 画像の保存
            cv2.imwrite(save_path, dst)
            print(f"⭕ 調整が完了しました。 '{save_path}'")
        else:
            # 顔が検出できなかったらそのまま保存する
            cv2.imwrite(save_path, resized_image)
            print(f"❌ 検出に失敗したので元画像のまま保存しました。 '{save_path}'")


if __name__ == "__main__":
    main()
