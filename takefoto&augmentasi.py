import cv2
import mediapipe as mp
import os
import random
import numpy as np
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import imgaug.augmenters as iaa

# ========== PARAMETER AUGMENTASI ==========
num_augmented = 500  # Jumlah gambar augmentasi per wajah

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

def get_random_augmenter():
    aug_list = random.sample(random_augmentations(), k=random.randint(3, 5))
    return iaa.Sequential(aug_list)

def augment_and_save(image, folder_path, base_filename):
    image = cv2.resize(image, (160, 160))
    for i in range(num_augmented):
        augmenter = get_random_augmenter()
        augmented = augmenter(image=image)
        filename_aug = f"{base_filename}_aug{i+1}.jpg"
        path_aug = os.path.join(folder_path, filename_aug)
        cv2.imwrite(path_aug, augmented)
    print(f"✅ Augmentasi selesai: {base_filename} -> {num_augmented} gambar baru")

# ========== FUNGSI AMBIL FOTO DAN AUGMENTASI ==========
def mulai_kamera():
    nama = entry.get().strip()
    if not nama:
        messagebox.showwarning("Peringatan", "Masukkan nama terlebih dahulu!")
        return

    root.destroy()  # Tutup jendela Tkinter

    output_root = 'foto'
    folder_nama = os.path.join(output_root, nama)
    os.makedirs(folder_nama, exist_ok=True)

    cap = cv2.VideoCapture(0)
    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)  # Ini menyebabkan efek mirror (kiri ↔ kanan)
            if not ret:
                print("❌ Gagal membaca kamera")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(frame_rgb)

            if results.detections:
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    x1 = int(bbox.xmin * w)
                    y1 = int(bbox.ymin * h)
                    box_width = int(bbox.width * w)
                    box_height = int(bbox.height * h)
                    x1 = max(0, x1)
                    y1 = max(0, y1)
                    x2 = min(w, x1 + box_width)
                    y2 = min(h, y1 + box_height)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)

            cv2.putText(frame, "Tekan SPASI untuk ambil foto, ESC untuk keluar", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.imshow("Ambil Foto", frame)

            key = cv2.waitKey(1)
            if key == 27:  # ESC
                break
            elif key == 32:  # SPACE
                if results.detections:
                    detection = results.detections[0]
                    bbox = detection.location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    x1 = int(bbox.xmin * w)
                    y1 = int(bbox.ymin * h)
                    box_width = int(bbox.width * w)
                    box_height = int(bbox.height * h)
                    x1 = max(0, x1)
                    y1 = max(0, y1)
                    x2 = min(w, x1 + box_width)
                    y2 = min(h, y1 + box_height)

                    face_crop = frame[y1:y2, x1:x2]
                    face_crop = cv2.resize(face_crop, (160, 160))
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{nama}_{timestamp}.jpg"
                    path_to_save = os.path.join(folder_nama, filename)
                    cv2.imwrite(path_to_save, face_crop)
                    print(f"✅ Wajah disimpan: {path_to_save}")

                    # Tambah augmentasi setelah simpan
                    augment_and_save(face_crop, folder_nama, f"{nama}_{timestamp}")

                    break  # keluar setelah foto diambil
                else:
                    print("⚠️ Tidak ada wajah terdeteksi!")

    cap.release()
    cv2.destroyAllWindows()

# ========== GUI TKINTER ==========
root = tk.Tk()
root.title("Input Nama")

label = tk.Label(root, text="Masukkan Nama:")
label.pack(padx=10, pady=10)

entry = tk.Entry(root)
entry.pack(padx=10, pady=5)
entry.focus()

button = tk.Button(root, text="Mulai Kamera", command=mulai_kamera)
button.pack(padx=10, pady=10)

root.mainloop()
