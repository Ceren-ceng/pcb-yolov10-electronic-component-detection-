from pathlib import Path
import shutil
import yaml

# Orijinal veri seti klasörü
SOURCE_DIR = Path("components_data_uncropped")

# Yeni temiz veri seti klasörü
TARGET_DIR = Path("components_data_clean_19")

# Çıkarılacak eski sınıf ID'leri
# 9  = heatsink
# 19 = transducer
# 20 = transformer
REMOVE_CLASS_IDS = {9, 19, 20}

# Orijinal sınıf isimleri
old_names = [
    'battery', 'button', 'buzzer', 'capacitor', 'clock', 'connector',
    'diode', 'display', 'fuse', 'heatsink', 'ic', 'inductor', 'led',
    'pads', 'pins', 'potentiometer', 'relay', 'resistor', 'switch',
    'transducer', 'transformer', 'transistor'
]

# Yeni sınıf listesi ve eski ID -> yeni ID dönüşümü
new_names = []
old_to_new_id = {}

for old_id, name in enumerate(old_names):
    if old_id not in REMOVE_CLASS_IDS:
        new_id = len(new_names)
        old_to_new_id[old_id] = new_id
        new_names.append(name)

print("Yeni sınıf sayısı:", len(new_names))
print("Yeni sınıflar:")
for i, name in enumerate(new_names):
    print(i, name)

# Önceden oluşturulmuş temiz klasör varsa sil
if TARGET_DIR.exists():
    shutil.rmtree(TARGET_DIR)

# Train / valid / test klasörlerini işle
for split in ["train", "valid", "test"]:
    source_images = SOURCE_DIR / split / "images"
    source_labels = SOURCE_DIR / split / "labels"

    target_images = TARGET_DIR / split / "images"
    target_labels = TARGET_DIR / split / "labels"

    target_images.mkdir(parents=True, exist_ok=True)
    target_labels.mkdir(parents=True, exist_ok=True)

    image_files = list(source_images.glob("*.*"))

    copied_images = 0
    kept_objects = 0
    removed_objects = 0

    for image_path in image_files:
        # Görseli yeni klasöre kopyala
        shutil.copy2(image_path, target_images / image_path.name)
        copied_images += 1

        label_path = source_labels / (image_path.stem + ".txt")
        target_label_path = target_labels / (image_path.stem + ".txt")

        new_lines = []

        if label_path.exists():
            lines = label_path.read_text(encoding="utf-8").splitlines()

            for line in lines:
                parts = line.strip().split()

                # YOLO etiketi: class_id x_center y_center width height
                if len(parts) < 5:
                    continue

                old_class_id = int(float(parts[0]))

                # Çıkarılacak sınıfsa bu etiketi atla
                if old_class_id in REMOVE_CLASS_IDS:
                    removed_objects += 1
                    continue

                # Kalan sınıfların ID'sini yeni 19 sınıflı sisteme göre değiştir
                new_class_id = old_to_new_id[old_class_id]
                parts[0] = str(new_class_id)

                new_lines.append(" ".join(parts))
                kept_objects += 1

        # Boş olsa bile label dosyası oluştur
        target_label_path.write_text("\n".join(new_lines), encoding="utf-8")

    print(f"\n{split.upper()}")
    print("Kopyalanan görüntü:", copied_images)
    print("Kalan nesne:", kept_objects)
    print("Silinen nesne:", removed_objects)

# Yeni data.yaml oluştur
data_yaml = {
    "path": str(TARGET_DIR.resolve()).replace("\\", "/"),
    "train": "train/images",
    "val": "valid/images",
    "test": "test/images",
    "nc": len(new_names),
    "names": new_names
}

with open(TARGET_DIR / "data.yaml", "w", encoding="utf-8") as f:
    yaml.dump(data_yaml, f, allow_unicode=True, sort_keys=False)

print("\nTemiz veri seti oluşturuldu:")
print(TARGET_DIR / "data.yaml")