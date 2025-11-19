SRC_CORE = """\"\"\"
 AdaptVec Core - Word-Specific Dimension Selection
 License: CC BY-NC-ND 4.0 - No commercial use, no derivatives
 \"\"\"
 import numpy as np
 from sklearn.metrics.pairwise import cosine_similarity
 import pickle
 from typing import Dict, List, Optional
 from dataclasses import dataclass
 import time
 @dataclass
 class AnlamVektoru:
    id: int
    label: str
    vektor: np.ndarray
    tags: List[str]
    anahtar_kelimeler: List[str]
 @dataclass
 class KelimeVerisi:
    kelime: str
    anlam_sayisi: int
    optimal_boyut: int
    kritik_boyutlar: List[int]
    anlamlar: Dict[str, AnlamVektoru]
 @dataclass
 class TahminSonucu:
    kelime: str
    tahmin_id: int
    tahmin_label: str
    guven_skoru: float
    hesaplama_suresi_ms: float
    kullanilan_boyut_sayisi: int
 class HibritVektorSistemi:
    \"\"\"
    Word-Specific Dimension Selection (WSDS) system
    Each word uses its own optimal dimensions
    \"\"\"
    
    def __init__(self, tam_boyut: int = 1024):
        self.tam_boyut = tam_boyut
        self.vektor_deposu: Dict[str, KelimeVerisi] = {}
        self.kelime_indeksi: Dict[str, List[int]] = {}
    
    def kelime_ekle(
        self, 
        kelime: str, 
        anlamlar: Dict, 
        optimal_boyut: int, 
        kritik_boyutlar: List[int]
    ):
        anlam_vektorleri = {}
        id_listesi = []
        
        for anlam_adi, anlam_bilgi in anlamlar.items():
            if anlam_bilgi['vektor'].shape[0] != self.tam_boyut:
                raise ValueError(f"Vector must be {self.tam_boyut} dimensions")
            
            anlam_vek = AnlamVektoru(
                id=anlam_bilgi['id'],
                label=anlam_bilgi['label'],
                vektor=anlam_bilgi['vektor'],
                tags=anlam_bilgi.get('tags', []),
                anahtar_kelimeler=anlam_bilgi.get('anahtar_kelimeler', [])
            )
            anlam_vektorleri[anlam_adi] = anlam_vek
            id_listesi.append(anlam_bilgi['id'])
        
        kelime_data = KelimeVerisi(
            kelime=kelime,
            anlam_sayisi=len(anlamlar),
            optimal_boyut=optimal_boyut,
            kritik_boyutlar=kritik_boyutlar,
            anlamlar=anlam_vektorleri
        )
        
        self.vektor_deposu[kelime] = kelime_data
        self.kelime_indeksi[kelime] = id_listesi
    
    def tahmin_yap(
        self, 
        kelime: str, 
        baglam_vektoru: Optional[np.ndarray] = None
    ) -> TahminSonucu:
        start_time = time.time()
        
        if kelime not in self.vektor_deposu:
            raise ValueError(f"Word '{kelime}' not found")
        
        kelime_data = self.vektor_deposu[kelime]
        
        if baglam_vektoru is None:
            ilk_anlam = list(kelime_data.anlamlar.values())[0]
            sure = (time.time() - start_time) * 1000
            return TahminSonucu(
                kelime=kelime,
                tahmin_id=ilk_anlam.id,
                tahmin_label=ilk_anlam.label,
                guven_skoru=0.5,
                hesaplama_suresi_ms=sure,
                kullanilan_boyut_sayisi=0
            )
        
        if baglam_vektoru.shape[0] != self.tam_boyut:
            raise ValueError(f"Context vector must be {self.tam_boyut} dimensions")
        
        # WSDS: Use word-specific dimensions
        kritik_boyutlar = kelime_data.kritik_boyutlar
        baglam_secili = baglam_vektoru[kritik_boyutlar]
        baglam_secili = baglam_secili / np.linalg.norm(baglam_secili)
        
        en_iyi_anlam = None
        en_yuksek_skor = -1
        
        for anlam_adi, anlam_data in kelime_data.anlamlar.items():
            anlam_secili = anlam_data.vektor[kritik_boyutlar]
            anlam_secili = anlam_secili / np.linalg.norm(anlam_secili)
            benzerlik = np.dot(baglam_secili, anlam_secili)
            
            if benzerlik > en_yuksek_skor:
                en_yuksek_skor = benzerlik
                en_iyi_anlam = anlam_data
        
        sure = (time.time() - start_time) * 1000
        
        return TahminSonucu(
            kelime=kelime,
            tahmin_id=en_iyi_anlam.id,
            tahmin_label=en_iyi_anlam.label,
            guven_skoru=float(en_yuksek_skor),
            hesaplama_suresi_ms=sure,
            kullanilan_boyut_sayisi=len(kritik_boyutlar)
        )
    
    def kaydet(self, dosya_yolu: str):
        with open(dosya_yolu, 'wb') as f:
            pickle.dump({
                'vektor_deposu': self.vektor_deposu,
                'kelime_indeksi': self.kelime_indeksi,
                'tam_boyut': self.tam_boyut
            }, f)
    
    def yukle(self, dosya_yolu: str):
        with open(dosya_yolu, 'rb') as f:
            data = pickle.load(f)
            self.vektor_deposu = data['vektor_deposu']
            self.kelime_indeksi = data['kelime_indeksi']
            self.tam_boyut = data['tam_boyut']
    
    def istatistikler(self) -> Dict:
        if not self.vektor_deposu:
            return {}
        
        boyut_sayilari = [k.optimal_boyut for k in self.vektor_deposu.values()]
        
        return {
            'toplam_kelime': len(self.vektor_deposu),
            'toplam_anlam': sum(k.anlam_sayisi for k in self.vektor_deposu.values()),
            'ortalama_boyut': np.mean(boyut_sayilari),
            'min_boyut': np.min(boyut_sayilari),
            'max_boyut': np.max(boyut_sayilari),
            'ortalama_tasarruf_yuzde': ((1024 - np.mean(boyut_sayilari)) / 1024) * 
100
        }
 """