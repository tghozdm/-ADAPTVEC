SRC_OPTIMIZER = """\"\"\"
 Fisher LDA Dimension Optimizer
 License: CC BY-NC-ND 4.0 - No commercial use, no derivatives
 \"\"\"
 import numpy as np
 from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Tuple, List
 class BoyutOptimizasyon:
    def __init__(self, tam_boyut: int = 1024, hedef_accuracy: float = 0.95):
        self.tam_boyut = tam_boyut
        self.hedef_accuracy = hedef_accuracy
    
    def egitim_verisi_olustur(self, anlam_sayisi: int, ornek_per_anlam: int = 200) -> 
Dict:
        veri = {'egitim': {}, 'test': {}, 'validasyon': {}, 'merkezler': []}
        
        for anlam_idx in range(anlam_sayisi):
            merkez = np.zeros(self.tam_boyut)
            baslangic = anlam_idx * (self.tam_boyut // anlam_sayisi)
            bitis = (anlam_idx + 1) * (self.tam_boyut // anlam_sayisi)
            
            merkez[baslangic:bitis] = np.random.randn(bitis - baslangic) * 3
            diger = list(range(0, baslangic)) + list(range(bitis, self.tam_boyut))
            merkez[diger] = np.random.randn(len(diger)) * 0.1
            merkez = merkez / np.linalg.norm(merkez)
            veri['merkezler'].append(merkez)
            
            egitim_ratio = 0.7
            test_ratio = 0.15
            
            egitim_sayisi = int(ornek_per_anlam * egitim_ratio)
            test_sayisi = int(ornek_per_anlam * test_ratio)
            validasyon_sayisi = ornek_per_anlam - egitim_sayisi - test_sayisi
            
            egitim = []
            for _ in range(egitim_sayisi):
                ornek = merkez + np.random.randn(self.tam_boyut) * 0.08
                ornek = ornek / np.linalg.norm(ornek)
                egitim.append(ornek)
            
            test = []
            for _ in range(test_sayisi):
                ornek = merkez + np.random.randn(self.tam_boyut) * 0.08
                ornek = ornek / np.linalg.norm(ornek)
                test.append(ornek)
            
            validasyon = []
            for _ in range(validasyon_sayisi):
                ornek = merkez + np.random.randn(self.tam_boyut) * 0.08
                ornek = ornek / np.linalg.norm(ornek)
                validasyon.append(ornek)
            
            veri['egitim'][anlam_idx] = np.array(egitim)
            veri['test'][anlam_idx] = np.array(test)
            veri['validasyon'][anlam_idx] = np.array(validasyon)
        
        veri['merkezler'] = np.array(veri['merkezler'])
        return veri
    
    def fisher_lda_skorlari(self, egitim_verisi: Dict, anlam_sayisi: int) -> 
Tuple[np.ndarray, np.ndarray]:
        boyut_skorlari = np.zeros(self.tam_boyut)
        
        for boyut_idx in range(self.tam_boyut):
            class_means = []
            class_vars = []
            
            for anlam_idx in range(anlam_sayisi):
                vals = egitim_verisi['egitim'][anlam_idx][:, boyut_idx]
                class_means.append(np.mean(vals))
                class_vars.append(np.var(vals))
            
            between_var = np.var(class_means)
            within_var = np.mean(class_vars)
            
            if within_var > 0:
                boyut_skorlari[boyut_idx] = between_var / within_var
        
        if np.max(boyut_skorlari) > 0:
            boyut_skorlari = boyut_skorlari / np.max(boyut_skorlari)
        
        sirali_boyutlar = np.argsort(boyut_skorlari)[::-1]
        return sirali_boyutlar, boyut_skorlari
    
    def optimal_boyut_bul(self, veri: Dict, sirali_boyutlar: np.ndarray, 
anlam_sayisi: int) -> Tuple[int, float]:
        merkezler = veri['merkezler']
        test_verisi = veri['test']
        
        baslangic_tahmin = max(int(anlam_sayisi * 15.8 + 6.2), 20)
        en_iyi_boyut = None
        en_iyi_accuracy = 0
        
        test_noktalari = list(range(baslangic_tahmin, min(300, self.tam_boyut), 10))
        
        for boyut_sayisi in test_noktalari:
            secili_boyutlar = sorted(sirali_boyutlar[:boyut_sayisi].tolist())
            accuracy = self._accuracy_hesapla(test_verisi, merkezler, 
secili_boyutlar)
            
            if accuracy >= self.hedef_accuracy:
                en_iyi_boyut = boyut_sayisi
                en_iyi_accuracy = accuracy
                break
            
            if accuracy > en_iyi_accuracy:
                en_iyi_accuracy = accuracy
                en_iyi_boyut = boyut_sayisi
        
        if en_iyi_boyut is None:
            en_iyi_boyut = test_noktalari[-1]
        
        return en_iyi_boyut, en_iyi_accuracy
    
    def _accuracy_hesapla(self, test_verisi: Dict, merkezler: np.ndarray, 
secili_boyutlar: List[int]) -> float:
        X_test = []
        y_test = []
        
        for anlam_idx, test_data in test_verisi.items():
            X_test.extend(test_data)
            y_test.extend([anlam_idx] * len(test_data))
        
        X_test = np.array(X_test)
        y_test = np.array(y_test)
        
        X_test_secili = X_test[:, secili_boyutlar]
        merkezler_secili = merkezler[:, secili_boyutlar]
        
        tahminler = []
        for ornek in X_test_secili:
            benzerlikler = cosine_similarity([ornek], merkezler_secili)[0]
            tahmin = np.argmax(benzerlikler)
            tahminler.append(tahmin)
        
        tahminler = np.array(tahminler)
        accuracy = np.sum(tahminler == y_test) / len(y_test)
        return accuracy
 """