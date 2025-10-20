# DOSYA KILAVUZU

Bu döküman, projedeki her dosyanın ne işe yaradığını açıklar.

## 📁 1_scripts/ - Python Scriptleri

### smart_contract.py (8 KB)
**Ne yapar:** Etherscan API kullanarak smart contract verilerini toplar
**Girdiler:** Etherscan API Key
**Çıktılar:** 
- smart_contracts_dataset.json (legit kontratlar)
- smart_contracts_dataset.csv

**Ne zaman çalıştırılır:** Proje başında, veri toplamak için

---

### manual_scam_data.py (8 KB)
**Ne yapar:** Scam ve vulnerable kontrat verilerini manuel olarak oluşturur
**Girdiler:** Yok (hardcoded data)
**Çıktılar:**
- scam_contracts.json (3 scam)
- vulnerable_contracts.json (3 vulnerable)
- vulnerability_patterns.json (pattern database)
- scam_keywords.json (scam detection keywords)

**Ne zaman çalıştırılır:** Veri toplama aşamasında

---

### dataset_merger.py (4.6 KB)
**Ne yapar:** Tüm veri kaynaklarını birleştirir
**Girdiler:** 
- smart_contracts_dataset.json
- scam_contracts.json
- vulnerable_contracts.json
**Çıktılar:**
- final_dataset.json (16 kontrat)
- final_dataset.csv
- dataset_report.txt

**Ne zaman çalıştırılır:** Veri toplama tamamlandıktan sonra

---

### vulnerability_analyzer.py (12 KB)
**Ne yapar:** Kontrat kodlarını NLP ile analiz edip vulnerability tespit eder
**Girdiler:** final_dataset.json
**Çıktılar:**
- vulnerability_analysis_results.json
- vulnerability_analysis_results.csv
- vulnerability_report.txt

**Ne zaman çalıştırılır:** Dataset hazır olduktan sonra

**Analiz edilen vulnerability'ler:**
- Reentrancy
- Integer Overflow
- tx.origin
- delegatecall
- selfdestruct
- Unchecked return values
- Access control

---

### arxiv_paper_collector.py (7.7 KB)
**Ne yapar:** arXiv API ile academic paper'ları otomatik toplar
**Girdiler:** Search query (smart contract security)
**Çıktılar:**
- academic_papers.json (15 paper)
- academic_papers_report.txt

**Ne zaman çalıştırılır:** Academic analiz için

---

### topic_modeling_analyzer.py (14 KB)
**Ne yapar:** Academic paper'lara topic modeling ve keyword analizi uygular
**Girdiler:** academic_papers.json
**Çıktılar:**
- academic_analysis_results.json
- academic_analysis_report.txt

**Kullandığı NLP teknikleri:**
- LDA (Latent Dirichlet Allocation)
- Keyword frequency analysis
- Topic modeling

**Ne zaman çalıştırılır:** Paper'lar toplandıktan sonra


## 📁 2_raw_data/ - Ham Veri Dosyaları

### smart_contracts_dataset.json (355 KB)
**İçeriği:** 10 legit kontratın tam source code'u
**Kontratlar:** Uniswap, USDT, USDC, Chainlink, WETH, DAI, Compound, AAVE, MakerDAO

---

### scam_contracts.json (1.4 KB)
**İçeriği:** 3 bilinen scam kontratın detayları
**Kontratlar:** SQUID Token, AnubisDAO, SaveTheKids

---

### vulnerable_contracts.json (1.7 KB)
**İçeriği:** 3 bilinen vulnerable kontratın detayları
**Kontratlar:** TheDAO, Parity MultiSig, BNB Bridge

---

### vulnerability_patterns.json (2 KB)
**İçeriği:** 7 vulnerability pattern tanımı
**Pattern'ler:** reentrancy, tx.origin, delegatecall, selfdestruct, overflow, etc.

---

### scam_keywords.json (413 B)
**İçeriği:** Scam detection için keyword'ler
**Kategoriler:** red_flags, suspicious_patterns

---

### academic_papers.json (26 KB)
**İçeriği:** 15 academic paper'ın metadata'sı
**Bilgiler:** title, abstract, authors, date, URL

---

## 📁 3_processed_data/ - İşlenmiş Veriler

### final_dataset.json (357 KB)
**İçeriği:** 16 kontratın TÜMÜ (legit + scam + vulnerable)
**Kullanım:** Ana dataset, tüm analizlerde kullanılır

---

### vulnerability_analysis_results.json (5.1 KB)
**İçeriği:** Her kontratın vulnerability analiz sonuçları
**Alanlar:**
- address
- name
- category
- vulnerabilities (list)
- risk_score (0-100)
- vulnerability_count

---

### vulnerability_analysis_results.csv (2.8 KB)
**İçeriği:** Aynı veri CSV formatında
**Kullanım:** Excel'de açmak, pandas ile analiz

---

### academic_analysis_results.json (3.2 KB)
**İçeriği:** Topic modeling sonuçları
**Alanlar:**
- vulnerability_mentions
- defense_recommendations
- topics

---

### enhanced_academic_results.json (547 B)
**İçeriği:** Gelişmiş academic analiz sonuçları
**Alanlar:**
- vulnerability_focus
- defense_mechanisms
- research_themes

---

## 📁 4_reports/ - Analiz Raporları

### dataset_report.txt (1.3 KB)
**İçeriği:** Dataset özeti
- Toplam kontrat sayısı
- Kategori dağılımı
- Sonraki adımlar

---

### vulnerability_report.txt (2.9 KB)
**İçeriği:** Vulnerability analiz özeti
- Risk dağılımı
- Top 5 risky contracts
- Vulnerability type distribution

---

### academic_papers_report.txt (4.5 KB)
**İçeriği:** Toplanan paper'ların listesi
- Paper detayları (title, authors, date)
- Keyword istatistikleri

---

### enhanced_academic_report.txt (YENİ)
**İçeriği:** Final academic analiz raporu
- Vulnerability focus
- Defense mechanisms
- Research trends
- Theory vs Practice comparison
- Practical recommendations

**EN ÖNEMLİ RAPOR** - Sunum için bunu kullan!

---

## 🎯 HANGİ DOSYALARI KULLANMALIYIM?

### Sunum/Rapor için:
✅ enhanced_academic_report.txt (en detaylı)
✅ vulnerability_report.txt
✅ final_dataset.csv (tablolar için)

### Veri analizi için:
✅ final_dataset.json (tüm kontratlar)
✅ vulnerability_analysis_results.csv (vulnerability sonuçları)
✅ enhanced_academic_results.json (academic analiz)

### Kod çalıştırmak için:
✅ 1_scripts/ klasöründeki .py dosyaları

---

## 🗑️ SİLİNEBİLECEK DOSYALAR

Eğer disk alanı lazımsa, şunlar silinebilir (backup al önce!):

❌ smart_contracts_dataset.json/csv (final_dataset'te var)
❌ academic_analysis_results.json (enhanced_academic_results'ta var)
❌ academic_papers_report.txt (enhanced'ta var)

**UYARI:** Silmeden önce mutlaka yedek al!

---

## 📊 DOSYA BOYUTLARI

Toplam: ~1.4 MB

En büyük dosyalar:
1. final_dataset.json (357 KB) - Ana dataset
2. smart_contracts_dataset.json (355 KB) - Ham veri
3. final_dataset.csv (342 KB) - CSV format
4. smart_contracts_dataset.csv (341 KB) - CSV format

---

## 🔄 WORKFLOW ÖZET

```
1. smart_contract.py 
   → smart_contracts_dataset.json

2. manual_scam_data.py 
   → scam_contracts.json
   → vulnerable_contracts.json

3. dataset_merger.py 
   → final_dataset.json ⭐

4. vulnerability_analyzer.py 
   → vulnerability_analysis_results.csv ⭐

5. arxiv_paper_collector.py 
   → academic_papers.json

6. enhanced_academic_analyzer.py 
   → enhanced_academic_report.txt ⭐

⭐ = En önemli çıktılar
```

---

## ❓ HÂLÂ SORULARIN MI VAR?

Her dosya için detaylı açıklama burada. Eğer hala bir dosyanın ne işe yaradığını anlamadıysan, dosya adını söyle, açıklayayım! 😊
