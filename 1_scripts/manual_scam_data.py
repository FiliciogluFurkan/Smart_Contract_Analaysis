"""
Manuel Scam ve Vulnerable Kontrat Verileri
Verified olmayan scam'ler için manual data oluşturuyoruz
"""

import json
from datetime import datetime

# Bilinen scam kontratları (verified olmasa da)
scam_data = [
    {
        'address': '0x87230146E138d3F296a9a77e497A2A83012e9Bc5',
        'name': 'SQUID Token',
        'category': 'scam',
        'scam_type': 'honeypot',
        'description': 'Squid Game token - users could buy but not sell (honeypot mechanism)',
        'known_vulnerabilities': ['honeypot', 'sell_restriction', 'hidden_mint'],
        'date_identified': '2021-11',
        'estimated_loss': '$3.38M',
        'verified': False,
        'source_notes': 'Rug pull scam - developers removed liquidity'
    },
    {
        'address': '0x5a3e6A77ba2f983eC0d371ea3B475F8Bc0811AD5',
        'name': 'AnubisDAO',
        'category': 'scam',
        'scam_type': 'rug_pull',
        'description': 'DeFi project that disappeared with investor funds within 24 hours',
        'known_vulnerabilities': ['rug_pull', 'liquidity_drain'],
        'date_identified': '2021-10',
        'estimated_loss': '$58M',
        'verified': False,
        'source_notes': 'Developer wallet drained all funds'
    },
    {
        'address': '0xB8c77482e45F1F44dE1745F52C74426C631bDD52',
        'name': 'SaveTheKids Token',
        'category': 'scam',
        'scam_type': 'pump_and_dump',
        'description': 'Celebrity-endorsed pump and dump scheme',
        'known_vulnerabilities': ['pump_and_dump', 'insider_selling'],
        'date_identified': '2021-06',
        'estimated_loss': '$1M+',
        'verified': False,
        'source_notes': 'Influencers promoted then sold immediately'
    }
]

# Bilinen vulnerable ama legit kontratlar (hacklenmiş)
vulnerable_data = [
    {
        'address': '0xbb9bc244d798123fde783fcc1c72d3bb8c189413',
        'name': 'TheDAO',
        'category': 'vulnerable',
        'vulnerability_type': 'reentrancy',
        'description': 'First major reentrancy attack on Ethereum',
        'known_vulnerabilities': ['reentrancy', 'recursive_call'],
        'date_identified': '2016-06',
        'estimated_loss': '$60M (at the time)',
        'verified': True,
        'source_notes': 'Led to Ethereum hard fork (ETH/ETC split)',
        'vulnerability_pattern': 'call.value()() before state update'
    },
    {
        'address': '0x863df6bfa4469f3ead0be8f9f2aae51c91a907b4',
        'name': 'Parity MultiSig Wallet',
        'category': 'vulnerable',
        'vulnerability_type': 'delegatecall',
        'description': 'Library self-destruct vulnerability',
        'known_vulnerabilities': ['delegatecall', 'selfdestruct', 'unprotected_function'],
        'date_identified': '2017-11',
        'estimated_loss': '$280M frozen',
        'verified': True,
        'source_notes': 'User accidentally killed library contract',
        'vulnerability_pattern': 'public delegatecall to library'
    },
    {
        'address': '0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552',
        'name': 'BNB Bridge Exploit',
        'category': 'vulnerable',
        'vulnerability_type': 'verification_bypass',
        'description': 'Cross-chain bridge verification exploit',
        'known_vulnerabilities': ['signature_verification', 'bridge_exploit'],
        'date_identified': '2022-10',
        'estimated_loss': '$570M',
        'verified': True,
        'source_notes': 'Forged proof to mint BNB tokens',
        'vulnerability_pattern': 'weak signature verification'
    }
]

# Common vulnerability patterns (NLP analizi için)
vulnerability_patterns = {
    'reentrancy': {
        'keywords': ['call.value', 'call()', 'send()', 'transfer() after state change'],
        'code_patterns': [
            'call.value()()',
            'address.call.value',
            'external call before state update'
        ],
        'description': 'External calls before state updates allow recursive exploitation'
    },
    'tx_origin': {
        'keywords': ['tx.origin', 'tx.origin authentication'],
        'code_patterns': ['require(tx.origin == owner)', 'if(tx.origin'],
        'description': 'Using tx.origin for authentication is vulnerable to phishing'
    },
    'delegatecall': {
        'keywords': ['delegatecall', 'delegatecall to untrusted'],
        'code_patterns': ['delegatecall(', 'address.delegatecall'],
        'description': 'Delegatecall to untrusted contracts can hijack storage'
    },
    'selfdestruct': {
        'keywords': ['selfdestruct', 'suicide'],
        'code_patterns': ['selfdestruct(', 'suicide('],
        'description': 'Unprotected selfdestruct can destroy contracts'
    },
    'unchecked_return': {
        'keywords': ['call without check', 'send without check'],
        'code_patterns': ['address.call(', 'address.send(', 'without checking return'],
        'description': 'Not checking return values can hide failures'
    },
    'overflow': {
        'keywords': ['overflow', 'underflow', 'integer overflow'],
        'code_patterns': ['uint addition', 'uint subtraction without SafeMath'],
        'description': 'Integer overflow/underflow before Solidity 0.8.0'
    },
    'honeypot': {
        'keywords': ['hidden owner', 'onlyOwner sell', 'transfer restriction'],
        'code_patterns': ['require(msg.sender == owner) in transfer', 'hidden ownership'],
        'description': 'Mechanisms that prevent users from selling tokens'
    }
}

# Scam description keywords (proje açıklamaları için)
scam_keywords = {
    'red_flags': [
        'guaranteed returns', 'risk-free', 'double your money',
        'limited time', 'act now', 'exclusive opportunity',
        'celebrity endorsed', 'get rich quick', 'passive income guaranteed'
    ],
    'suspicious_patterns': [
        'no whitepaper', 'anonymous team', 'no audit',
        'locked liquidity claims without proof', 'unrealistic APY'
    ]
}

def save_all_data():
    """Tüm manual verileri kaydet"""
    
    # Scam data
    with open('scam_contracts.json', 'w', encoding='utf-8') as f:
        json.dump(scam_data, f, indent=2, ensure_ascii=False)
    
    # Vulnerable data
    with open('vulnerable_contracts.json', 'w', encoding='utf-8') as f:
        json.dump(vulnerable_data, f, indent=2, ensure_ascii=False)
    
    # Vulnerability patterns
    with open('vulnerability_patterns.json', 'w', encoding='utf-8') as f:
        json.dump(vulnerability_patterns, f, indent=2, ensure_ascii=False)
    
    # Scam keywords
    with open('scam_keywords.json', 'w', encoding='utf-8') as f:
        json.dump(scam_keywords, f, indent=2, ensure_ascii=False)
    
    print("✅ Manuel veri dosyaları oluşturuldu:")
    print(f"   📄 scam_contracts.json ({len(scam_data)} scam)")
    print(f"   📄 vulnerable_contracts.json ({len(vulnerable_data)} vulnerable)")
    print(f"   📄 vulnerability_patterns.json ({len(vulnerability_patterns)} pattern)")
    print(f"   📄 scam_keywords.json")
    
    # İstatistikler
    print("\n📊 Veri Özeti:")
    print(f"   🚨 Scam Kontratlar: {len(scam_data)}")
    print(f"   ⚠️  Vulnerable Kontratlar: {len(vulnerable_data)}")
    print(f"   🔍 Vulnerability Pattern'leri: {len(vulnerability_patterns)}")
    
    # Toplam loss
    total_scam_loss = sum([float(s['estimated_loss'].replace('$','').replace('M','').replace('+','')) 
                          for s in scam_data if 'M' in s['estimated_loss']])
    total_vuln_loss = sum([float(v['estimated_loss'].replace('$','').replace('M','').split()[0]) 
                          for v in vulnerable_data if 'M' in v['estimated_loss']])
    
    print(f"\n💰 Toplam Kayıp Tahminleri:")
    print(f"   Scam'ler: ~${total_scam_loss:.1f}M")
    print(f"   Vulnerabilities: ~${total_vuln_loss:.0f}M")

if __name__ == "__main__":
    save_all_data()