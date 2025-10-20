"""
Academic Paper Collector - arXiv API
Smart contract security paper'larını otomatik toplar
"""

import requests
import xml.etree.ElementTree as ET
import json
import time
from datetime import datetime

class ArxivPaperCollector:
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        self.papers = []
    
    def search_papers(self, query="smart contract security", max_results=15):
        """arXiv'den paper'ları ara"""
        
        print(f"🔍 Searching arXiv for: '{query}'")
        print(f"📊 Max results: {max_results}\n")
        
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # XML parse et
            root = ET.fromstring(response.content)
            
            # Namespace tanımla
            ns = {'atom': 'http://www.w3.org/2005/Atom',
                  'arxiv': 'http://arxiv.org/schemas/atom'}
            
            entries = root.findall('atom:entry', ns)
            
            print(f"✅ Found {len(entries)} papers\n")
            print("="*70)
            
            for idx, entry in enumerate(entries, 1):
                # Paper bilgilerini çıkar
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                published = entry.find('atom:published', ns).text[:10]
                link = entry.find('atom:id', ns).text
                
                # Yazarlar
                authors = []
                for author in entry.findall('atom:author', ns):
                    name = author.find('atom:name', ns).text
                    authors.append(name)
                
                # Kategoriler
                categories = []
                for category in entry.findall('atom:category', ns):
                    cat = category.get('term')
                    categories.append(cat)
                
                paper = {
                    'id': idx,
                    'title': title,
                    'authors': authors,
                    'abstract': summary,
                    'published_date': published,
                    'arxiv_url': link,
                    'categories': categories
                }
                
                self.papers.append(paper)
                
                # Progress göster
                print(f"\n📄 Paper {idx}/{len(entries)}")
                print(f"Title: {title[:80]}...")
                print(f"Authors: {', '.join(authors[:3])}{'...' if len(authors) > 3 else ''}")
                print(f"Published: {published}")
                print(f"Abstract: {summary[:150]}...")
                print("-"*70)
                
                # Rate limit (arXiv istemiyor ama nazik olalım)
                time.sleep(0.5)
            
            return self.papers
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def extract_keywords(self):
        """Paper'lardan güvenlik keyword'lerini çıkar"""
        
        security_keywords = [
            'reentrancy', 'overflow', 'underflow', 'access control',
            'tx.origin', 'delegatecall', 'selfdestruct', 'timestamp',
            'front-running', 'integer overflow', 'authorization',
            'vulnerability', 'exploit', 'audit', 'formal verification',
            'static analysis', 'symbolic execution'
        ]
        
        keyword_counts = {kw: 0 for kw in security_keywords}
        
        for paper in self.papers:
            abstract_lower = paper['abstract'].lower()
            title_lower = paper['title'].lower()
            
            for keyword in security_keywords:
                if keyword in abstract_lower or keyword in title_lower:
                    keyword_counts[keyword] += 1
        
        # Sırala
        sorted_keywords = sorted(keyword_counts.items(), 
                                key=lambda x: x[1], 
                                reverse=True)
        
        print("\n" + "="*70)
        print("🔑 TOP SECURITY KEYWORDS IN PAPERS")
        print("="*70)
        
        for keyword, count in sorted_keywords:
            if count > 0:
                percentage = (count / len(self.papers)) * 100
                bar = "█" * int(percentage / 5)
                print(f"{keyword:<20} : {count:>2} papers ({percentage:>5.1f}%) {bar}")
        
        return sorted_keywords
    
    def save_papers(self, filename='../2_raw_data/academic_papers.json'):
        """Paper'ları kaydet"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.papers, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Papers saved to: {filename}")
    
    def generate_report(self):
        """Özet rapor oluştur"""
        
        if not self.papers:
            print("⚠️ No papers to report")
            return
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          ACADEMIC PAPERS COLLECTION REPORT                   ║
╚══════════════════════════════════════════════════════════════╝

📊 COLLECTION STATISTICS
{'─'*60}
Total Papers Collected: {len(self.papers)}
Date Range: {min(p['published_date'] for p in self.papers)} to {max(p['published_date'] for p in self.papers)}

📚 PAPERS LIST
{'─'*60}
"""
        
        for paper in self.papers:
            report += f"\n{paper['id']}. {paper['title']}\n"
            report += f"   Authors: {', '.join(paper['authors'][:2])}{'...' if len(paper['authors']) > 2 else ''}\n"
            report += f"   Date: {paper['published_date']}\n"
            report += f"   URL: {paper['arxiv_url']}\n"
        
        report += f"""
{'─'*60}

✅ Next Steps:
   1. Review collected papers
   2. Run topic modeling analysis
   3. Extract security recommendations
   4. Compare with real-world contracts

"""
        
        print(report)
        
        with open('../4_reports/academic_papers_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("📄 Report saved: academic_papers_report.txt")


def main():
    """Ana fonksiyon"""
    
    print("🚀 Starting Academic Paper Collection\n")
    
    collector = ArxivPaperCollector()
    
    # Paper'ları topla
    papers = collector.search_papers(
        query="smart contract security vulnerability blockchain",
        max_results=15
    )
    
    if papers:
        # Keyword analizi
        collector.extract_keywords()
        
        # Kaydet
        collector.save_papers()
        
        # Rapor oluştur
        collector.generate_report()
        
        print("\n✅ Collection completed successfully!")
        print(f"📦 Collected {len(papers)} papers")
        print("\n📝 Next: Run topic modeling on these papers")
    else:
        print("❌ No papers collected")


if __name__ == "__main__":
    main()