import cv2
import mediapipe as mp
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Inisialisasi MediaPipe
mp_face_detection = mp.solutions.face_detection

# Fungsi untuk mulai kamera setelah input nama
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

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        while True:
            ret, frame = cap.read()
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
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

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
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{nama}_{timestamp}.jpg"
                    path_to_save = os.path.join(folder_nama, filename)
                    cv2.imwrite(path_to_save, face_crop)
                    print(f"✅ Wajah disimpan: {path_to_save}")
                    break  # keluar setelah foto diambil
                else:
                    print("⚠️ Tidak ada wajah terdeteksi!")

    cap.release()
    cv2.destroyAllWindows()

# GUI Tkinter
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
