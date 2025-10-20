# Smart Contract Security Analysis via NLP

## 📋 Proje Özeti
Bu proje, Ethereum akıllı sözleşmelerinin güvenlik analizini Natural Language Processing (NLP) teknikleri kullanarak gerçekleştirmektedir.

## 🗂️ Klasör Yapısı

```
smartContracts/
├── 1_scripts/              # Python scriptleri
├── 2_raw_data/            # Ham veri dosyaları
├── 3_processed_data/      # İşlenmiş veriler
├── 4_reports/             # Analiz raporları
├── FILE_GUIDE.md          # Detaylı dosya açıklamaları
└── README.md              # Bu dosya
```

## 🚀 Nasıl Çalıştırılır

### Adım 1: Veri Toplama
```bash
python 1_scripts/smart_contract.py
python 1_scripts/manual_scam_data.py
```

### Adım 2: Vulnerability Analizi
```bash
python 1_scripts/vulnerability_analyzer.py
```

### Adım 3: Academic Paper Analizi
```bash
python 1_scripts/arxiv_paper_collector.py
python 1_scripts/enhanced_academic_analyzer.py
```

## 📊 Sonuçlar

- **16 smart contract** analiz edildi (10 legit, 3 scam, 3 vulnerable)
- **15 academic paper** toplandı ve analiz edildi
- **13 vulnerability** tespit edildi
- **Theory vs Practice** karşılaştırması yapıldı

## 🎯 Önemli Bulgular

1. Popüler kontratların %60'ı güvenlik riski taşıyor
2. En yaygın vulnerability: Integer overflow
3. Academic öneriler pratikte yeterince uygulanmıyor
4. %100 academic paper reentrancy guard öneriyor

## 👥 Ekip

- Enis Buğra Okunakol
- Furkan Filicioğlu

## 📅 Tarih

Ekim 2025 - Gebze Technical University
