# CICIoV2024 Veri Setinde Ezber ve Kısayol Öğrenme

Bu depo, *"CICIoV2024 Veri Setinde Ezber ve Kısayol Öğrenme: CAN Bus Saldırı Tespiti Değerlendirmesinin Eleştirel Bir Analizi"* başlıklı bildirinin kodunu ve sonuç tablolarını içerir.

**Kısaca:** CICIoV2024'te raporlanan %99–100 başarılar büyük ölçüde iki şeyi ölçer: (1) %99,75 tekrar nedeniyle **ezber**, (2) saldırıların normal trafikte bulunmayan ID'ler kullanması nedeniyle **ID kısayolu**. Basit bir birebir eşleşme tablosu, rastgele bölmede Random Forest ve LightGBM ile aynı makro F1 değerini (1,000) alır. Görülmemiş saldırı senaryolarında tespit oranı %57'ye, ID bilgisi olmadan %37'ye düşer.

## Veri

Veri seti bu depoda **yoktur**. [UNB CIC sayfasından](https://www.unb.ca/cic/datasets/iov-dataset-2024.html) indirip `decimal` klasöründeki 6 CSV dosyasını kullanın:

```
decimal_benign.csv
decimal_DoS.csv
decimal_spoofing-GAS.csv
decimal_spoofing-RPM.csv
decimal_spoofing-SPEED.csv
decimal_spoofing-STEERING_WHEEL.csv
```

> Neto, E. C. P. vd. (2024). CICIoV2024: Advancing realistic IDS approaches against DoS and spoofing attack in IoV CAN bus. *Internet of Things*, 26, 101209.

## İçerik

| Dosya | Ne yapar | Araştırma sorusu |
|---|---|---|
| `notebooks/01_veri_kesfi.ipynb` | Sınıf dağılımı, tekrar oranı, sınıflar arası çakışma, rastgele bölmede sızıntı, CAN ID analizi | AS1 |
| `notebooks/02_deneyler.ipynb` | Rastgele bölmede modeller ve önemsiz temel çizgiler; ID analizi; tek sınıflı anomali tespiti; saldırı türü dışarıda bırakma | AS2, AS3 |
| `notebooks/03_sirali_bolme.ipynb` | Orijinal makalenin sıralı bölmesi ile rastgele bölmenin karşılaştırması | AS2 |
| `scripts/sekilleri_ciz.py` | Bildirideki 4 şekli üretir (PNG + PDF) | – |
| `sonuclar/` | Deneylerin ham ve özet tabloları | – |
| `sekiller/` | Bildiri şekilleri | – |

## Çalıştırma

Not defterleri Google Colab için yazılmıştır. Her not defterinin ilk kod hücresindeki `DATA_DIR` değişkenini CSV dosyalarının bulunduğu klasöre ayarlayın. Yerel çalıştırmada `drive.mount` satırlarını silmeniz yeterlidir.

```bash
pip install -r requirements.txt
python scripts/sekilleri_ciz.py
```

Tüm deneyler 5 tohumla (0–4) tekrarlanmıştır. `02_deneyler.ipynb` içindeki rastgele bölme deneyleri 1,4 milyon satırla Colab'da yaklaşık 30–60 dakika sürer; `SAMPLE_FRAC` ile örneklenebilir.

## Temel bulgular

| Bulgu | Değer |
|---|---|
| Benzersiz satır oranı | 3.588 / 1.408.219 (%0,25) |
| Benzersiz saldırı çerçevesi | DoS 21, RPM 10, SPEED 5, STEERING_WHEEL 3, GAS 2 |
| Rastgele %80/20 bölmede test satırlarının eğitimde birebir bulunma oranı | %99,80 (saldırılarda %100) |
| Ezber tablosu makro F1 (rastgele / sıralı bölme) | 1,000 / 0,519 |
| Random Forest makro F1 (rastgele / sıralı bölme; orijinal makale 0,76) | 1,000 / 0,721 |
| Saldırı ID'lerinden normal trafikte bulunan | 0 / 5 |
| ID beyaz listesi ile görülmemiş saldırı tespiti | %100 (yanlış alarm %1,5) |
| Random Forest, saldırı türü dışarıda bırakılarak (ID + veri / yalnızca veri) | %56,8 / %36,5 |
| DoS, yalnızca veri baytlarıyla (LOF / RF) | %0 / %5,7 |

## Lisans

Kod MIT lisansı ile paylaşılmıştır. Veri setinin kullanım koşulları için UNB CIC sayfasına bakın.

---

*English summary:* This repository audits the CICIoV2024 CAN bus intrusion detection dataset. 99.75% of rows are exact duplicates; under the random 80/20 split used by most prior work, 100% of attack test rows also appear in training, and an exact-match lookup table reaches macro-F1 = 1.000, matching Random Forest and LightGBM. None of the five CAN IDs used by attacks appear in benign traffic, so an ID whitelist detects all attacks. Reproducing the original paper's sequential split lowers Random Forest to macro-F1 0.72 (original: 0.76) and the lookup table to 0.52. Under leakage-free unseen-attack protocols, detection drops to 56.8% (37% without the ID feature), and DoS cannot be detected from payload alone.
