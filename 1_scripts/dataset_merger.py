"""
Tüm veri kaynaklarını birleştir ve final dataset oluştur
"""

import json
import pandas as pd

def merge_all_datasets():
    """Etherscan, manual scam ve vulnerable verileri birleştir"""
    
    all_contracts = []
    
    # 1. Etherscan'den toplanan verified kontratlar
    try:
        with open('smart_contracts_dataset.json', 'r', encoding='utf-8') as f:
            etherscan_data = json.load(f)
            all_contracts.extend(etherscan_data)
            print(f"✅ Etherscan'den {len(etherscan_data)} kontrat yüklendi")
    except FileNotFoundError:
        print("⚠️  smart_contracts_dataset.json bulunamadı")
    
    # 2. Manuel scam kontratlar
    try:
        with open('scam_contracts.json', 'r', encoding='utf-8') as f:
            scam_data = json.load(f)
            all_contracts.extend(scam_data)
            print(f"✅ {len(scam_data)} scam kontrat eklendi")
    except FileNotFoundError:
        print("⚠️  scam_contracts.json bulunamadı")
    
    # 3. Vulnerable kontratlar
    try:
        with open('vulnerable_contracts.json', 'r', encoding='utf-8') as f:
            vuln_data = json.load(f)
            all_contracts.extend(vuln_data)
            print(f"✅ {len(vuln_data)} vulnerable kontrat eklendi")
    except FileNotFoundError:
        print("⚠️  vulnerable_contracts.json bulunamadı")
    
    # Final dataset kaydet
    with open('final_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(all_contracts, f, indent=2, ensure_ascii=False)
    
    # CSV formatında da kaydet
    df = pd.DataFrame(all_contracts)
    df.to_csv('final_dataset.csv', index=False, encoding='utf-8')
    
    # İstatistikler
    print("\n" + "="*50)
    print("📊 FİNAL DATASET İSTATİSTİKLERİ")
    print("="*50)
    print(f"\n✅ Toplam Kontrat: {len(all_contracts)}")
    
    if 'category' in df.columns:
        print("\n📁 Kategorilere Göre Dağılım:")
        category_counts = df['category'].value_counts()
        for cat, count in category_counts.items():
            emoji = "🔒" if cat == "legit" else ("🚨" if cat == "scam" else "⚠️")
            print(f"   {emoji} {cat.capitalize()}: {count}")
    
    # Verified/Unverified oranı
    if 'verified' in df.columns:
        verified_count = df['verified'].sum() if df['verified'].dtype == bool else len(df[df['verified'] == True])
        print(f"\n✓ Verified: {verified_count}")
        print(f"✗ Unverified: {len(df) - verified_count}")
    
    # Source code var mı kontrol
    has_source = len(df[df['source_code'].notna()]) if 'source_code' in df.columns else 0
    print(f"\n📝 Source Code Olan: {has_source}")
    
    print("\n💾 Dosyalar kaydedildi:")
    print("   📄 final_dataset.json")
    print("   📄 final_dataset.csv")
    print("\n" + "="*50)
    
    return df

def generate_summary_report(df):
    """Özet rapor oluştur"""
    
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║          SMART CONTRACT SECURITY DATASET RAPORU              ║
╚══════════════════════════════════════════════════════════════╝

📊 GENEL İSTATİSTİKLER
{'─'*60}
Toplam Kontrat Sayısı: {len(df)}

📁 KATEGORİ DAĞILIMI
{'─'*60}
"""
    
    if 'category' in df.columns:
        for cat, count in df['category'].value_counts().items():
            percentage = (count / len(df)) * 100
            report += f"{cat.upper():<15} : {count:>3} ({percentage:>5.1f}%)\n"
    
    report += f"""
{'─'*60}

✅ SONRAKİ ADIMLAR:
  1. ✓ Veri toplama tamamlandı
  2. → GitHub proje açıklamaları topla
  3. → Vulnerability analizi yap
  4. → NLP modelleme
  5. → Sonuçları raporla

"""
    
    with open('dataset_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print("📄 Rapor kaydedildi: dataset_report.txt")

if __name__ == "__main__":
    print("🔄 Dataset'ler birleştiriliyor...\n")
    df = merge_all_datasets()
    generate_summary_report(df)
    
    print("\n✅ Veri birleştirme tamamlandı!")
    print("\n💡 Şimdi ne yapabiliriz:")
    print("   A) GitHub scraper ile proje açıklamaları topla")
    print("   B) Vulnerability pattern analizi yap")
    print("   C) Academic paper'ları topla")