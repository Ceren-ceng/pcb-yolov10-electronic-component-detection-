from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ==============================
# KLASÖR YOLLARI
# ==============================

TRAIN_RUN_DIR = Path("runs/detect/pcb_yolov10s_19cls_960_final")
TEST_RUN_DIR = Path("runs/detect/pcb_yolov10s_19cls_960_test")

OUTPUT_DIR = Path("final_rapor_ciktilari")
OUTPUT_DIR.mkdir(exist_ok=True)

# ==============================
# TEST SONUÇLARI
# Bu değerler terminalde aldığımız final test çıktısından girildi.
# ==============================

rows = [
    ["all", 122, 3933, 0.729, 0.667, 0.687, 0.439],
    ["battery", 8, 8, 0.536, 0.625, 0.693, 0.540],
    ["button", 4, 18, 0.569, 0.589, 0.502, 0.320],
    ["buzzer", 7, 8, 0.885, 0.967, 0.926, 0.756],
    ["capacitor", 77, 1337, 0.897, 0.812, 0.858, 0.561],
    ["clock", 10, 16, 0.699, 0.725, 0.786, 0.321],
    ["connector", 40, 228, 0.633, 0.579, 0.565, 0.349],
    ["diode", 34, 91, 0.681, 0.549, 0.594, 0.376],
    ["display", 13, 14, 0.707, 0.863, 0.899, 0.609],
    ["fuse", 5, 20, 1.000, 0.879, 0.895, 0.444],
    ["ic", 66, 514, 0.820, 0.825, 0.845, 0.586],
    ["inductor", 25, 57, 0.561, 0.298, 0.393, 0.256],
    ["led", 31, 113, 0.747, 0.628, 0.633, 0.308],
    ["pads", 6, 43, 0.591, 0.209, 0.236, 0.144],
    ["pins", 1, 14, 0.427, 0.357, 0.247, 0.159],
    ["potentiometer", 10, 12, 0.673, 0.750, 0.799, 0.553],
    ["relay", 6, 10, 0.919, 0.900, 0.895, 0.701],
    ["resistor", 72, 1300, 0.846, 0.785, 0.826, 0.516],
    ["switch", 18, 53, 0.840, 0.811, 0.856, 0.557],
    ["transistor", 28, 77, 0.816, 0.520, 0.608, 0.281],
]

df = pd.DataFrame(
    rows,
    columns=[
        "class_name",
        "images",
        "instances",
        "precision_kesinlik",
        "recall_yakalama_orani",
        "map50",
        "map50_95",
    ],
)

# ==============================
# EK METRİKLER
# ==============================

# F1 skoru = precision ve recall dengesini gösterir.
df["f1_skoru"] = (
    2
    * df["precision_kesinlik"]
    * df["recall_yakalama_orani"]
    / (df["precision_kesinlik"] + df["recall_yakalama_orani"])
)

# Yaklaşık TP / FP / FN hesapları
# Not: Bunlar terminaldeki precision/recall değerlerinden yaklaşık türetilmiştir.
df["yaklasik_TP_dogru_pozitif"] = df["recall_yakalama_orani"] * df["instances"]
df["yaklasik_FN_yanlis_negatif"] = df["instances"] - df["yaklasik_TP_dogru_pozitif"]
df["yaklasik_FP_yanlis_pozitif"] = df["yaklasik_TP_dogru_pozitif"] * (
    (1 / df["precision_kesinlik"].replace(0, np.nan)) - 1
)

df["tespit_dogrulugu_accuracy"] = df["yaklasik_TP_dogru_pozitif"] / (
    df["yaklasik_TP_dogru_pozitif"]
    + df["yaklasik_FP_yanlis_pozitif"]
    + df["yaklasik_FN_yanlis_negatif"]
)

# ==============================
# CSV ÇIKTILARI
# ==============================

df.to_csv(OUTPUT_DIR / "sinif_bazli_test_performansi.csv", index=False, encoding="utf-8-sig")

summary = df[df["class_name"] == "all"].copy()
summary.to_csv(OUTPUT_DIR / "genel_test_ozeti.csv", index=False, encoding="utf-8-sig")

# ==============================
# GRAFİK 1: SINIF DAĞILIMI
# ==============================

class_df = df[df["class_name"] != "all"].copy()
class_df = class_df.sort_values("instances", ascending=True)

plt.figure(figsize=(10, 8))
plt.barh(class_df["class_name"], class_df["instances"])
plt.xlabel("Nesne Sayısı")
plt.ylabel("Sınıf")
plt.title("Test Seti Sınıf Dağılımı")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_test_sinif_dagilimi.png", dpi=300)
plt.close()

# ==============================
# GRAFİK 2: PRECISION / RECALL / F1
# ==============================

metric_df = df[df["class_name"] != "all"].copy()
metric_df = metric_df.sort_values("f1_skoru", ascending=True)

x = np.arange(len(metric_df))
width = 0.25

plt.figure(figsize=(14, 7))
plt.bar(x - width, metric_df["precision_kesinlik"], width, label="Precision (Kesinlik)")
plt.bar(x, metric_df["recall_yakalama_orani"], width, label="Recall (Yakalama Oranı)")
plt.bar(x + width, metric_df["f1_skoru"], width, label="F1 Skoru")
plt.xticks(x, metric_df["class_name"], rotation=60, ha="right")
plt.ylim(0, 1.05)
plt.ylabel("Skor")
plt.title("Sınıf Bazlı Precision, Recall ve F1 Skoru")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_precision_recall_f1.png", dpi=300)
plt.close()

# ==============================
# GRAFİK 3: mAP50 ve mAP50-95
# ==============================

map_df = df[df["class_name"] != "all"].copy()
map_df = map_df.sort_values("map50", ascending=True)

x = np.arange(len(map_df))
width = 0.35

plt.figure(figsize=(14, 7))
plt.bar(x - width / 2, map_df["map50"], width, label="mAP50")
plt.bar(x + width / 2, map_df["map50_95"], width, label="mAP50-95")
plt.xticks(x, map_df["class_name"], rotation=60, ha="right")
plt.ylim(0, 1.05)
plt.ylabel("Skor")
plt.title("Sınıf Bazlı mAP50 ve mAP50-95")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_map_skorlari.png", dpi=300)
plt.close()

# ==============================
# GRAFİK 4: EN ZAYIF SINIFLAR
# ==============================

weak_df = df[df["class_name"] != "all"].copy()
weak_df = weak_df.sort_values("map50", ascending=True).head(8)

plt.figure(figsize=(10, 6))
plt.barh(weak_df["class_name"], weak_df["map50"])
plt.xlabel("mAP50")
plt.ylabel("Sınıf")
plt.title("mAP50 Değerine Göre En Zayıf Sınıflar")
plt.xlim(0, 1)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_en_zayif_siniflar.png", dpi=300)
plt.close()

# ==============================
# GRAFİK 5: EĞİTİM SÜRECİ GRAFİKLERİ
# ==============================

results_csv = TRAIN_RUN_DIR / "results.csv"

if results_csv.exists():
    train_df = pd.read_csv(results_csv)
    train_df.columns = [col.strip() for col in train_df.columns]

    # Loss grafiği
    plt.figure(figsize=(10, 6))
    plt.plot(train_df["epoch"], train_df["train/box_loss"], label="Train Box Loss (Kutu Hatası)")
    plt.plot(train_df["epoch"], train_df["train/cls_loss"], label="Train Class Loss (Sınıf Hatası)")
    plt.plot(train_df["epoch"], train_df["train/dfl_loss"], label="Train DFL Loss (Kutu Hassasiyet Hatası)")
    plt.xlabel("Epoch (Eğitim Turu)")
    plt.ylabel("Loss (Hata)")
    plt.title("Eğitim Hata Değerleri")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_egitim_loss_grafigi.png", dpi=300)
    plt.close()

    # Başarı metrikleri
    precision = train_df["metrics/precision(B)"]
    recall = train_df["metrics/recall(B)"]
    f1 = 2 * precision * recall / (precision + recall)

    plt.figure(figsize=(10, 6))
    plt.plot(train_df["epoch"], precision, label="Precision (Kesinlik)")
    plt.plot(train_df["epoch"], recall, label="Recall (Yakalama Oranı)")
    plt.plot(train_df["epoch"], f1, label="F1 Skoru")
    plt.xlabel("Epoch (Eğitim Turu)")
    plt.ylabel("Skor")
    plt.title("Eğitim Boyunca Precision, Recall ve F1")
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "06_egitim_precision_recall_f1.png", dpi=300)
    plt.close()

    # mAP grafiği
    plt.figure(figsize=(10, 6))
    plt.plot(train_df["epoch"], train_df["metrics/mAP50(B)"], label="mAP50")
    plt.plot(train_df["epoch"], train_df["metrics/mAP50-95(B)"], label="mAP50-95")
    plt.xlabel("Epoch (Eğitim Turu)")
    plt.ylabel("Skor")
    plt.title("Eğitim Boyunca mAP Değerleri")
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "07_egitim_map_grafigi.png", dpi=300)
    plt.close()

# ==============================
# TXT RAPOR ÖZETİ
# ==============================

overall = df[df["class_name"] == "all"].iloc[0]

report_text = f"""
YOLOv10s PCB Bileşen Tespiti Final Test Özeti

Model:
YOLOv10s

Veri seti:
19 sınıflı temiz PCB bileşen veri seti

Test görüntüsü sayısı:
{int(overall["images"])}

Test nesne sayısı:
{int(overall["instances"])}

Genel Precision (Kesinlik):
{overall["precision_kesinlik"]:.3f}

Genel Recall (Yakalama Oranı):
{overall["recall_yakalama_orani"]:.3f}

Genel F1 Skoru:
{overall["f1_skoru"]:.3f}

Genel mAP50:
{overall["map50"]:.3f}

Genel mAP50-95:
{overall["map50_95"]:.3f}

Yaklaşık Tespit Doğruluğu:
{overall["tespit_dogrulugu_accuracy"]:.3f}

Yorum:
Model, PCB üzerindeki elektronik bileşenleri genel olarak başarılı şekilde tespit etmektedir.
Özellikle capacitor, resistor, ic, switch, display, buzzer ve relay sınıflarında güçlü sonuçlar alınmıştır.
Pads ve pins gibi küçük ve ince yapılı sınıflarda performans düşmektedir.
Bu durum, PCB görüntülerinde küçük nesne tespitinin zor olmasından kaynaklanmaktadır.
"""

(OUTPUT_DIR / "final_test_raporu.txt").write_text(report_text, encoding="utf-8")

print("Analiz tamamlandı.")
print(f"Çıktılar şu klasöre kaydedildi: {OUTPUT_DIR.resolve()}")