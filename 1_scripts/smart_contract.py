"""
Smart Contract Security Analysis - Data Collection Module
Bu script Etherscan'den kontrat verilerini toplar
"""

import requests
import pandas as pd
import time
import json
from datetime import datetime
import os

class ContractCollector:
    def __init__(self, api_key):
        """
        Etherscan API key ile initialize et
        Ücretsiz key: https://etherscan.io/myapikey
        """
        self.api_key = api_key
        self.base_url = "https://api.etherscan.io/v2/api"  # V2 API kullan
        self.contracts_data = []
        
    def get_contract_source(self, contract_address):
        """Kontrat source code'unu çek"""
        params = {
            'chainid': '1',  # Ethereum mainnet
            'module': 'contract',
            'action': 'getsourcecode',
            'address': contract_address,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            print(f"🔍 Checking {contract_address[:10]}...")
            print(f"   API Response: {data}")
            
            if data['status'] == '1' and data['result'] and len(data['result']) > 0 and data['result'][0].get('SourceCode'):
                print(f"   ✅ Source code bulundu!")
                return {
                    'address': contract_address,
                    'name': data['result'][0]['ContractName'],
                    'source_code': data['result'][0]['SourceCode'],
                    'compiler_version': data['result'][0]['CompilerVersion'],
                    'optimization': data['result'][0]['OptimizationUsed'],
                    'license': data['result'][0].get('LicenseType', 'Unknown')
                }
            else:
                print(f"   ⚠️ Source code bulunamadı veya verified değil")
            return None
        except Exception as e:
            print(f"   ❌ Error fetching {contract_address}: {e}")
            return None
    
    def collect_verified_contracts(self, num_contracts=10):
        """Verified kontratları topla"""
        print("📥 Verified kontratlar toplanıyor...")
        
        # Son verified kontratları çek
        params = {
            'chainid': '1',  # Ethereum mainnet
            'module': 'contract',
            'action': 'listcontracts',
            'page': 1,
            'offset': num_contracts,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if data['status'] == '1':
                for contract in data['result']:
                    time.sleep(0.2)  # API rate limit
                    contract_data = self.get_contract_source(contract['ContractAddress'])
                    if contract_data:
                        contract_data['category'] = 'unknown'
                        contract_data['collection_date'] = datetime.now().isoformat()
                        self.contracts_data.append(contract_data)
                        print(f"✅ {contract_data['name']} - {contract_data['address'][:10]}...")
                        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def add_known_contracts(self):
        """Bilinen güvenli ve scam kontratları ekle"""
        
        # Güvenli / Popüler Kontratlar
        legit_contracts = {
            'Uniswap V2 Router': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
            'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
            'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
            'Chainlink': '0x514910771AF9Ca656af840dff83E8264EcF986CA',
            'Wrapped Ether': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
            'DAI Stablecoin': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
            'Uniswap V3 Router': '0xE592427A0AEce92De3Edee1F18E0157C05861564',
            'Compound USDC': '0x39AA39c021dfbaE8faC545936693aC917d5E7563',
            'AAVE Lending Pool': '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9',
            'Maker DAO': '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2',
        }
        
        print("\n🔒 Güvenli kontratlar ekleniyor...")
        for name, address in legit_contracts.items():
            time.sleep(0.2)
            contract_data = self.get_contract_source(address)
            if contract_data:
                contract_data['category'] = 'legit'
                contract_data['collection_date'] = datetime.now().isoformat()
                self.contracts_data.append(contract_data)
                print(f"✅ {name}")
        
        # Bilinen Scam/Vulnerable Kontratlar (örnekler)
        # NOT: Bunları güncel scam listelerinden toplayabilirsiniz
        risky_contracts = {
            # Örnek adresler - gerçek scam adresleri eklenebilir
            'Example Risky 1': '0x...',  # Gerçek adres eklenecek
        }
        
        print("\n⚠️ Risk içeren kontratlar için scam veritabanlarına bakın:")
        print("- ChainAbuse.com")
        print("- CryptoScamDB")
        print("- RugDoc")
        
        # Bilinen Scam Kontratlar (gerçek örnekler)
        scam_contracts = {
            'SQUID Token (Honeypot)': '0x87230146E138d3F296a9a77e497A2A83012e9Bc5',  # Ünlü Squid Game scam
        }
        
        print("\n🚨 Scam kontratlar ekleniyor...")
        for name, address in scam_contracts.items():
            time.sleep(0.2)
            contract_data = self.get_contract_source(address)
            if contract_data:
                contract_data['category'] = 'scam'
                contract_data['collection_date'] = datetime.now().isoformat()
                self.contracts_data.append(contract_data)
                print(f"⚠️ {name}")
            else:
                print(f"⚠️ {name} - Source code verified değil (scam olduğu için normal)")
    
    def save_data(self, filename='contracts_data.json'):
        """Toplanan veriyi kaydet"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.contracts_data, f, indent=2, ensure_ascii=False)
        
        # CSV olarak da kaydet
        df = pd.DataFrame(self.contracts_data)
        csv_filename = filename.replace('.json', '.csv')
        df.to_csv(csv_filename, index=False)
        
        print(f"\n💾 Veri kaydedildi:")
        print(f"   - {filename}")
        print(f"   - {csv_filename}")
        print(f"   Toplam: {len(self.contracts_data)} kontrat")
    
    def get_statistics(self):
        """Toplanan veri istatistikleri"""
        df = pd.DataFrame(self.contracts_data)
        print("\n📊 Toplanan Veri İstatistikleri:")
        print(f"Toplam Kontrat: {len(df)}")
        if 'category' in df.columns:
            print("\nKategorilere Göre Dağılım:")
            print(df['category'].value_counts())


# ============= KULLANIM ÖRNEĞİ =============

def main():
    """Ana fonksiyon - buradan çalıştırın"""
    
    # 1. API KEY'inizi buraya girin
    API_KEY = "WGVRSVI4TIK7TRE31JDB1D8B8F2VQHMUWF"  # https://etherscan.io/myapikey
    
    if API_KEY == "YOUR_ETHERSCAN_API_KEY_HERE":
        print("⚠️  UYARI: Etherscan API key'inizi ekleyin!")
        print("👉 https://etherscan.io/myapikey adresinden ücretsiz alabilirsiniz")
        return
    
    # 2. Collector'ı başlat
    collector = ContractCollector(API_KEY)
    
    # 3. Bilinen güvenli kontratları ekle
    collector.add_known_contracts()
    
    # 4. Random verified kontratlar ekle (isteğe bağlı)
    # collector.collect_verified_contracts(num_contracts=10)
    
    # 5. Verileri kaydet
    collector.save_data('smart_contracts_dataset.json')
    
    # 6. İstatistikleri göster
    collector.get_statistics()
    
    print("\n✅ Veri toplama tamamlandı!")
    print("\n📝 Sonraki Adım:")
    print("   1. Scam kontrat adreslerini manuel olarak ekleyin")
    print("   2. GitHub'dan proje açıklamalarını toplayın")
    print("   3. Kontrat kodlarını analiz etmeye başlayın")


if __name__ == "__main__":
    main()