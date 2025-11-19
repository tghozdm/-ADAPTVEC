# -ADAPTVEC
 README_MD = """# AdaptVec
 > Word-Specific Dimension Selection for Word Sense Disambiguation
 [![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--
 ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
 [![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)]
 (https://www.python.org/downloads/)
 ## Core Innovation
 Traditional: **1024 → 80 dims (all words)**  
AdaptVec: **1024 → 45-100 dims (per word)**
 Each word uses its own optimal dimensions.
 ## Quick Start
 ```bash
 pip install -r requirements.txt
```
 ```python
 from src.core import HibritVektorSistemi
 from src.optimizer import BoyutOptimizasyon
 # Optimize
 optimizer = BoyutOptimizasyon(tam_boyut=1024)
 data = optimizer.egitim_verisi_olustur(anlam_sayisi=4)
 sorted_dims, _ = optimizer.fisher_lda_skorlari(data, 4)
 optimal, _ = optimizer.optimal_boyut_bul(data, sorted_dims, 4)
 critical = sorted(sorted_dims[:optimal].tolist())
 # Predict
 system = HibritVektorSistemi(tam_boyut=1024)
 system.kelime_ekle('word', senses, optimal, critical)
 result = system.tahmin_yap('word', context_vector)
 ```
 ## Performance- **12x faster** inference- **85% smaller** models- **<0.5% accuracy** los
