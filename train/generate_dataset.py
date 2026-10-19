import os
import json
import shutil
import random
from pathlib import Path

def generate_combined_yolo_dataset(
    base_dir='c:/Users/mp44l/Repositories/dwp-ppt-word',
    val_ratio=0.15,
    seed=42
):
    base_dir = Path(base_dir)
    out_dataset = base_dir / 'train/dataset_ppt'

    classes = ['Title', 'Subtitle', 'Plain Text', 'Picture', 'Caption Picture']
    class_to_id = {c: i for i, c in enumerate(classes)}

    sources = [
        {
            'name': 'dataset_prep1',
            'prefix': 'p1',
            'classif': base_dir / 'work/dataset_prep/classifications.json',
            'mapping': base_dir / 'work/dataset_prep/boxes_mapping.json',
            'images': base_dir / 'work/dataset_prep/images',
        },
        {
            'name': 'dataset_prep2',
            'prefix': 'p2',
            'classif': base_dir / 'work/dataset_prep2/classifications.json',
            'mapping': base_dir / 'work/dataset_prep2/boxes_mapping.json',
            'images': base_dir / 'work/dataset_prep2/images',
        }
    ]

    all_items = []

    for src in sources:
        if not src['classif'].exists() or not src['mapping'].exists():
            print(f"Skipping {src['name']} (files missing)")
            continue

        with open(src['classif'], 'r', encoding='utf-8') as f:
            classifications = json.load(f)
        with open(src['mapping'], 'r', encoding='utf-8') as f:
            mappings = json.load(f)

        print(f"Loaded {len(classifications)} slides from {src['name']}")

        for slide_name, slide_classif in classifications.items():
            all_items.append({
                'source': src['name'],
                'prefix': src['prefix'],
                'slide_name': slide_name,
                'classif': slide_classif,
                'mapping': mappings.get(slide_name, {}),
                'img_dir': src['images']
            })

    print(f"Total combined slides across datasets: {len(all_items)}")

    train_img_dir = out_dataset / 'images/train'
    val_img_dir = out_dataset / 'images/val'
    train_lbl_dir = out_dataset / 'labels/train'
    val_lbl_dir = out_dataset / 'labels/val'

    if out_dataset.exists():
        shutil.rmtree(out_dataset)

    train_img_dir.mkdir(parents=True, exist_ok=True)
    val_img_dir.mkdir(parents=True, exist_ok=True)
    train_lbl_dir.mkdir(parents=True, exist_ok=True)
    val_lbl_dir.mkdir(parents=True, exist_ok=True)

    random.seed(seed)
    random.shuffle(all_items)

    val_count = max(1, int(len(all_items) * val_ratio))
    val_indices = set(range(val_count))

    stats = {c: 0 for c in classes}
    total_written = 0

    for idx, item in enumerate(all_items):
        split = 'val' if idx in val_indices else 'train'
        target_img_dir = val_img_dir if split == 'val' else train_img_dir
        target_lbl_dir = val_lbl_dir if split == 'val' else train_lbl_dir

        prefix = item['prefix']
        slide_name = item['slide_name']
        unique_name = f"{prefix}_{slide_name}"

        img_path = item['img_dir'] / f"{slide_name}.png"
        if not img_path.exists():
            img_path = item['img_dir'] / f"{slide_name}.jpg"

        if not img_path.exists():
            print(f"Warning: Image {slide_name} not found in {item['img_dir']}")
            continue

        shutil.copy2(img_path, target_img_dir / f"{unique_name}{img_path.suffix}")

        slide_mapping = item['mapping']
        boxes_dict = slide_mapping.get('boxes', slide_mapping) if isinstance(slide_mapping, dict) else slide_mapping
        slide_classif = item['classif']

        lines = []
        for badge_id, class_name in slide_classif.items():
            if class_name not in class_to_id:
                continue
            c_id = class_to_id[class_name]
            box_info = boxes_dict.get(badge_id)
            if not box_info:
                continue
            yolo_box = box_info.get('yolo_box')
            if not yolo_box:
                continue
            x, y, w, h = yolo_box
            lines.append(f"{c_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
            stats[class_name] += 1

        with open(target_lbl_dir / f"{unique_name}.txt", 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        total_written += 1

    print("\n================ DATASET GENERATION SUMMARY ================")
    print(f"Total processed images: {total_written} ({total_written - val_count} train, {val_count} val)")
    print(f"Dataset directory: {out_dataset}")
    print(f"Total bounding boxes: {sum(stats.values())}")
    for c, count in stats.items():
        print(f"  - {c}: {count}")
    print("============================================================\n")

if __name__ == '__main__':
    generate_combined_yolo_dataset()
