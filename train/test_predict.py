from pathlib import Path
from ultralytics import YOLO

if __name__ == '__main__':
    # Cari weights best.pt terbaru di runs/detect/
    weights_candidates = list(Path('.').glob('runs/detect/**/weights/best.pt')) + list(Path('..').glob('runs/detect/**/weights/best.pt'))
    if weights_candidates:
        # Ambil yang paling baru dimodifikasi
        weights_path = max(weights_candidates, key=lambda p: p.stat().st_mtime)
        print(f"Menggunakan model: {weights_path}")
    else:
        weights_path = 'runs/detect/train-2/weights/best.pt'
        print(f"Default model path: {weights_path}")

    model = YOLO(str(weights_path))

    # Lakukan prediksi pada gambar slide baru
    results = model.predict(source='slide_baru_test.png', save=True, conf=0.25)

    print("\nSelesai! Cek folder runs/detect/predict untuk melihat gambar hasilnya.")