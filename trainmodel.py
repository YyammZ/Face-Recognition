import os
import numpy as np
from PIL import Image
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
import joblib
from tqdm import tqdm
import torch
from torchvision import transforms
from facenet_pytorch import InceptionResnetV1, MTCNN

# Inisialisasi FaceNet dan MTCNN (untuk deteksi wajah)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Fungsi untuk memuat dan mengonversi gambar ke embedding
def get_embedding(img_path):
    img = Image.open(img_path).convert('RGB')
    face = mtcnn(img)
    if face is None:
        return None
    face_embedding = resnet(face.unsqueeze(0).to(device))
    return face_embedding.detach().cpu().numpy()[0]

# Proses dataset
data_dir = 'augmented_dataset'
X, y = [], []

for class_name in os.listdir(data_dir):
    class_dir = os.path.join(data_dir, class_name)
    if not os.path.isdir(class_dir):
        continue
    for img_name in tqdm(os.listdir(class_dir), desc=f'Processing {class_name}'):
        img_path = os.path.join(class_dir, img_name)
        embedding = get_embedding(img_path)
        if embedding is not None:
            X.append(embedding)
            y.append(class_name)

# Encoding label dan melatih classifier
le = LabelEncoder()
y_encoded = le.fit_transform(y)
clf = SVC(kernel='linear', probability=True)

model = Pipeline([
    ('classifier', clf)
])
model.fit(X, y_encoded)

# Simpan model dan label encoder
output = {'model': model, 'label_encoder': le}
joblib.dump(output, 'model.pkl')

print("Model berhasil disimpan ke model.pkl")
