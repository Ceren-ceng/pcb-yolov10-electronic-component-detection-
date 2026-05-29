# PCB Electronic Component Detection using YOLOv10

## Proje Hakkında

Bu proje, Baskılı Devre Kartları (PCB - Printed Circuit Board) üzerinde bulunan elektronik bileşenlerin otomatik olarak tespit edilmesi amacıyla geliştirilmiştir. Çalışmada YOLOv10 tabanlı nesne tespit modelleri kullanılmış ve farklı model boyutlarının performansları karşılaştırılmıştır.

Proje kapsamında ham veri seti temizlenmiş, sınıf düzenlemeleri gerçekleştirilmiş, veri dağılımı analiz edilmiş ve YOLOv10n ile YOLOv10s modelleri eğitilerek performans değerlendirmeleri yapılmıştır.

---

## Amaç

PCB görüntüleri üzerinde bulunan elektronik bileşenlerin otomatik olarak tespit edilmesini sağlayan bir derin öğrenme modeli geliştirmek.

Tespit edilen bileşenler:

* Battery
* Button
* Buzzer
* Capacitor
* Clock
* Connector
* Diode
* Display
* Fuse
* IC
* Inductor
* LED
* Pads
* Pins
* Potentiometer
* Relay
* Resistor
* Switch
* Transistor

Toplam: **19 sınıf**

---

## Veri Seti

Bu çalışmada kullanılan veri seti Kaggle platformundan elde edilmiştir.

Veri Seti:

https://www.kaggle.com/datasets/akhatova/pcb-electronic-components-detection-dataset

Orijinal veri seti içerisinde bulunan bazı sınıflar veri dengesizliği ve proje kapsamı nedeniyle çıkarılmıştır.

Çıkarılan sınıflar:

* Heatsink
* Transducer
* Transformer

Böylece çalışma 19 sınıf üzerinden devam ettirilmiştir.

---

## Veri Seti Temizleme Süreci

Veri seti üzerinde aşağıdaki işlemler gerçekleştirilmiştir:

* Gereksiz sınıfların kaldırılması
* Sınıf ID'lerinin yeniden düzenlenmesi
* Etiket dosyalarının güncellenmesi
* Yeni YAML yapılandırmasının oluşturulması
* Eğitim için temiz veri setinin hazırlanması

Bu işlemler:

`clean_dataset_19.py`

dosyası kullanılarak gerçekleştirilmiştir.

---

## Kullanılan Modeller

### 1. YOLOv10n

İlk deneysel model olarak kullanılmıştır.

Amaç:

* Veri setini test etmek
* Sınıf problemlerini belirlemek
* Hata bölgelerini analiz etmek

### 2. YOLOv10s

YOLOv10n sonuçlarından elde edilen gözlemler doğrultusunda veri seti düzenlenmiş ve daha güçlü olan YOLOv10s modeli kullanılmıştır.

Amaç:

* Daha yüksek doğruluk
* Daha yüksek F1 skoru
* Daha iyi mAP performansı
* Sınıflar arası karışıklığı azaltmak

---

## Proje Dosyaları

### Veri Seti Analizi

`dataset_analiz.py`

Veri seti içerisindeki sınıf dağılımlarını analiz eder.

---

### Sınıf Dağılımı Analizi

`split_sinif_dagilimi.py`

Train / Validation / Test dağılımlarını üretir.

---

### Genel Performans Analizi

`final_analiz_raporu.py`

Model sonuçlarını analiz eder ve rapor çıktıları oluşturur.

---

### Hata Analizi

`hata_analizi_tablosu.py`

Düşük performans gösteren sınıfların hata analizlerini oluşturur.

---

## Eğitim Çıktıları

Eğitim sonuçları:

`runs/detect/`

klasörü içerisinde bulunmaktadır.

Önemli çıktılar:

* confusion_matrix.png
* confusion_matrix_normalized.png
* BoxPR_curve.png
* BoxF1_curve.png
* BoxP_curve.png
* BoxR_curve.png
* results.csv
* results.png
* train_batch*.jpg
* val_batch*_pred.jpg

---

## Model Dosyaları

### YOLOv10n

`yolov10n.pt`

### YOLOv10s

`yolov10s.pt`

---

## Test Sonuçları

YOLOv10s modeli ile elde edilen temel sonuçlar:

| Metrik       | Değer |
| ------------ | ----- |
| Precision    | 0.729 |
| Recall       | 0.667 |
| F1 Score     | 0.697 |
| mAP@0.5      | 0.687 |
| mAP@0.5:0.95 | 0.439 |

---

## Güçlü Sınıflar

* Buzzer
* Relay
* Fuse
* Capacitor
* Display
* Switch
* IC
* Resistor
* Potentiometer

---

## Zorlayıcı Sınıflar

* Pads
* Pins
* Inductor
* Connector
* Button
* Diode
* Transistor

Bu sınıflarda özellikle:

* küçük nesne boyutları
* yoğun PCB bölgeleri
* sınıflar arası görsel benzerlikler

tespit performansını olumsuz etkilemiştir.

---

## Kullanılan Teknolojiler

* Python
* YOLOv10
* Ultralytics
* OpenCV
* Pandas
* NumPy
* Matplotlib

---

## Sonuç

Bu çalışma kapsamında PCB görüntülerindeki elektronik bileşenlerin otomatik tespiti için YOLOv10 tabanlı bir sistem geliştirilmiştir.

İlk aşamada YOLOv10n modeli ile veri seti analiz edilmiş, tespit edilen eksiklikler giderilmiş ve ardından YOLOv10s modeli kullanılarak daha başarılı sonuçlar elde edilmiştir.

Elde edilen sonuçlar, PCB üretim süreçlerinde otomatik kalite kontrol, elektronik kart analizi ve akıllı üretim sistemleri gibi alanlarda kullanılabilecek bir yaklaşım ortaya koymaktadır.
