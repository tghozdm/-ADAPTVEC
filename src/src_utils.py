SRC_UTILS = """\"\"\"
 Utility functions
 License: CC BY-NC-ND 4.0 - No commercial use, no derivatives
 \"\"\"
 import numpy as np
def normalize_vektor(vektor: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vektor)
    if norm > 0:
        return vektor / norm
    return vektor
 def model_boyutu_hesapla(boyut: int, kelime_sayisi: int, anlam_per_kelime: float) -> 
float:
    \"\"\"Calculate model size in MB\"\"\"
    return (boyut * kelime_sayisi * anlam_per_kelime * 4) / (1024 * 1024)
 def tasarruf_hesapla(tam_boyut: int, optimal_boyut: int) -> float:
    \"\"\"Calculate dimension reduction percentage\"\"\"
    return ((tam_boyut - optimal_boyut) / tam_boyut) * 100
 """
 