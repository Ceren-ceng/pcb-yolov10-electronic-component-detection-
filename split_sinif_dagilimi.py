from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Sınıf isimleri
class_names = [
    "battery", "button", "buzzer", "capacitor", "clock",
    "connector", "diode", "display", "fuse", "ic",
    "inductor", "led", "pads", "pins", "potentiometer",
    "relay", "resistor", "switch", "transistor"
]

# Veri seti ana klasörü
dataset_dir = Path("components_data_clean_19")

splits = ["train", "valid", "test"]
rows = []

for split in splits:
    label_dir = dataset_dir / split / "labels"

    counts = {name: 0 for name in class_names}

    for label_file in label_dir.glob("*.txt"):
        with open(label_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    class_id = int(line.split()[0])
                    class_name = class_names[class_id]
                    counts[class_name] += 1

    for class_name, count in counts.items():
        rows.append({
            "split": split,
            "class": class_name,
            "count": count
        })

df = pd.DataFrame(rows)

# CSV olarak kaydet
output_dir = Path("final_report_ciktilari")
output_dir.mkdir(exist_ok=True)

csv_path = output_dir / "train_valid_test_sinif_dagilimi.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

# Pivot tablo
pivot_df = df.pivot(index="class", columns="split", values="count").fillna(0)
pivot_df = pivot_df[["train", "valid", "test"]]

# Grafik
pivot_df.plot(kind="bar", figsize=(16, 7))

plt.title("Train / Validation / Test Sınıf Dağılımı")
plt.xlabel("Sınıf")
plt.ylabel("Nesne Sayısı")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

png_path = output_dir / "08_train_valid_test_sinif_dagilimi.png"
plt.savefig(png_path, dpi=300)
plt.show()

print("CSV kaydedildi:", csv_path)
print("Grafik kaydedildi:", png_path)