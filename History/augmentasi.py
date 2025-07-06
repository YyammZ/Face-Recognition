import cv2
import os
import numpy as np
from imgaug import augmenters as iaa
import random

# Path input dan output
input_root = 'cropped_dataset'
output_root = 'augmented_dataset'
os.makedirs(output_root, exist_ok=True)

# Jumlah augmentasi per gambar
num_augmented = 812

import imgaug.augmenters as iaa
import random

# Fungsi pembuat augmentasi acak (baru tiap kali dipanggil)
def random_augmentations():
    return [
        iaa.Fliplr(1.0),
        iaa.GaussianBlur(sigma=(0.3, 2.0)),
        iaa.AdditiveGaussianNoise(scale=(5, 25)),
        iaa.Multiply((0.6, 1.4)),
        iaa.Affine(rotate=(-20, 20)),
        iaa.Affine(scale=(0.85, 1.15)),
        iaa.Affine(translate_percent={"x": (-0.15, 0.15), "y": (-0.15, 0.15)}),
        iaa.Add((-30, 30)),
        iaa.CoarseDropout((0.02, 0.1), size_percent=(0.02, 0.07)),
        iaa.LinearContrast((0.7, 1.4)),
    ]

# Setiap kali dipanggil, ini akan menghasilkan kombinasi augmentasi acak baru
def get_random_augmenter():
    aug_list = random.sample(random_augmentations(), k=random.randint(3, 5))
    return iaa.Sequential(aug_list)


# Proses semua gambar
for root, dirs, files in os.walk(input_root):
    for file in files:
        if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        input_path = os.path.join(root, file)
        image = cv2.imread(input_path)
        if image is None:
            print(f"❌ Tidak bisa membaca gambar: {input_path}")
            continue

        # Resize (opsional, jika kamu ingin hasil final ke ukuran tertentu)
        image = cv2.resize(image, (160, 160))

        # Buat path output sesuai struktur folder
        relative_path = os.path.relpath(root, input_root)
        output_folder = os.path.join(output_root, relative_path)
        os.makedirs(output_folder, exist_ok=True)

        # Simpan gambar asli
        original_out_path = os.path.join(output_folder, file)
        cv2.imwrite(original_out_path, image)

        # Augmentasi n kali
        for i in range(num_augmented):
            augmenter = get_random_augmenter()
            augmented = augmenter(image=image)
            out_filename = f"{os.path.splitext(file)[0]}_aug{i+1}.jpg"
            out_path = os.path.join(output_folder, out_filename)
            cv2.imwrite(out_path, augmented)

        print(f"✅ Augmentasi selesai: {file} -> {num_augmented} gambar baru")
