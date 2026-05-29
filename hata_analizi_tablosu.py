import pandas as pd
from pathlib import Path

rows = [
    {
        "Sınıf": "pads",
        "Sorun": "Düşük mAP ve düşük F1",
        "Olası Neden": "Çok küçük alan, yoğun PCB arka planı, annotation hassasiyeti",
        "Çözüm Önerisi": "Daha fazla pads örneği, crop tabanlı eğitim, daha yüksek çözünürlük"
    },
    {
        "Sınıf": "pins",
        "Sorun": "Sık kaçırma ve background ile karışma",
        "Olası Neden": "İnce yapı, birbirine çok yakın pin dizilimleri",
        "Çözüm Önerisi": "Yakın plan pin görüntüleri ekleme, etiket kalitesi kontrolü"
    },
    {
        "Sınıf": "inductor",
        "Sorun": "Orta-düşük tespit başarımı",
        "Olası Neden": "Farklı inductor tiplerinin görsel çeşitliliği",
        "Çözüm Önerisi": "Daha dengeli ve çeşitli inductor verisi"
    },
    {
        "Sınıf": "connector",
        "Sorun": "Resistor/capacitor/arka plan ile karışma",
        "Olası Neden": "Farklı connector formları ve yoğun PCB bölgeleri",
        "Çözüm Önerisi": "Connector alt tiplerini artırma, daha temiz etiketleme"
    },
    {
        "Sınıf": "capacitor / resistor / ic",
        "Sorun": "Yoğun sahnelerde aşırı tespit ve label crowding",
        "Olası Neden": "Bu sınıfların veri setinde baskın olması ve PCB üzerinde çok sık bulunması",
        "Çözüm Önerisi": "Dengeli veri seti, hard negative örnekler, yoğun bölge crop analizi"
    }
]

df = pd.DataFrame(rows)

output_dir = Path("final_report_ciktilari")
output_dir.mkdir(exist_ok=True)

df.to_csv(output_dir / "hata_analizi_tablosu.csv", index=False, encoding="utf-8-sig")

print("Hata analizi tablosu oluşturuldu.")