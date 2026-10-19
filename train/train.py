from ultralytics import YOLO

if __name__ == '__main__':
    # Load model YOLO11 paling modern dan stabil
    model = YOLO('yolo11n.pt') 

    results = model.train(
        data='data.yaml',
        epochs=50,
        imgsz=1024,
        batch=4,
        workers=2,
        device='0'
    )