from pathlib import Path
from collections import Counter
import yaml
import pandas as pd

DATASET_DIR = Path("components_data_uncropped")
YAML_PATH = DATASET_DIR / "data.yaml"

with open(YAML_PATH, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

names = data["names"]
if isinstance(names, list):
    class_names = {i: name for i, name in enumerate(names)}
else:
    class_names = {int(i): name for i, name in names.items()}

def analyze_split(split_name, label_folder):
    label_dir = DATASET_DIR / label_folder / "labels"
    image_dir = DATASET_DIR / label_folder / "images"

    image_count = len(list(image_dir.glob("*.*")))
    label_files = list(label_dir.glob("*.txt"))

    class_counter = Counter()
    empty_labels = 0
    total_objects = 0

    for txt in label_files:
        lines = txt.read_text(encoding="utf-8").strip().splitlines()
        if not lines:
            empty_labels += 1
            continue

        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                class_id = int(float(parts[0]))
                class_counter[class_id] += 1
                total_objects += 1

    rows = []
    for class_id, class_name in class_names.items():
        rows.append({
            "split": split_name,
            "class_id": class_id,
            "class_name": class_name,
            "object_count": class_counter[class_id]
        })

    return image_count, len(label_files), empty_labels, total_objects, rows

all_rows = []

for split_name, folder in [
    ("train", "train"),
    ("valid", "valid"),
    ("test", "test")
]:
    image_count, label_count, empty_labels, total_objects, rows = analyze_split(split_name, folder)
    print(f"\n{split_name.upper()}")
    print(f"Görüntü sayısı: {image_count}")
    print(f"Etiket dosyası sayısı: {label_count}")
    print(f"Boş etiket dosyası: {empty_labels}")
    print(f"Toplam nesne sayısı: {total_objects}")
    all_rows.extend(rows)

df = pd.DataFrame(all_rows)

pivot = df.pivot_table(
    index=["class_id", "class_name"],
    columns="split",
    values="object_count",
    fill_value=0
).reset_index()

pivot["total"] = pivot.get("train", 0) + pivot.get("valid", 0) + pivot.get("test", 0)
pivot = pivot.sort_values("total", ascending=False)

print("\nSINIF BAZLI NESNE SAYILARI:")
print(pivot.to_string(index=False))

pivot.to_csv("dataset_class_distribution.csv", index=False, encoding="utf-8-sig")
print("\nKaydedildi: dataset_class_distribution.csv")