EXAMPLES_BASIC = """\"\"\"
 AdaptVec - Basic Usage Example
 License: CC BY-NC-ND 4.0 - No commercial use, no derivatives
 \"\"\"
 from src.core import HibritVektorSistemi
 from src.optimizer import BoyutOptimizasyon
 import numpy as np
 def main():
    print("AdaptVec - Basic Usage Example")
    print("=" * 60)
    
    # 1. Initialize
    optimizer = BoyutOptimizasyon(tam_boyut=1024)
    system = HibritVektorSistemi(tam_boyut=1024)
    
    # 2. Generate data for word with 4 senses
    print("\\n1. Generating training data...")
    data = optimizer.egitim_verisi_olustur(anlam_sayisi=4)
    
    # 3. Find optimal dimensions
    print("2. Finding optimal dimensions...")
    sorted_dims, _ = optimizer.fisher_lda_skorlari(data, 4)
    optimal_dim, accuracy = optimizer.optimal_boyut_bul(data, sorted_dims, 4)
    critical_dims = sorted(sorted_dims[:optimal_dim].tolist())
    
    print(f"   Optimal dimensions: {optimal_dim}/1024")
    print(f"   Accuracy: {accuracy*100:.1f}%")
    print(f"   Reduction: {((1024-optimal_dim)/1024)*100:.1f}%")
    
    # 4. Add word to system
    print("\\n3. Adding word to system...")
    senses = {
        f'sense_{i}': {
            'id': i,
            'label': f'Sense {i}',
            'vektor': data['merkezler'][i],
            'tags': [f'tag{i}'],
            'anahtar_kelimeler': [f'keyword{i}']
        }
        for i in range(4)
    }
    
    system.kelime_ekle('example_word', senses, optimal_dim, critical_dims)
    
    # 5. Predict with context
    print("\\n4. Making prediction...")
    context_vector = data['test'][0][0]  # Use test sample
    result = system.tahmin_yap('example_word', context_vector)
    
    print(f"   Predicted sense: {result.tahmin_label}")
    print(f"   Confidence: {result.guven_skoru:.3f}")
    print(f"   Dimensions used: {result.kullanilan_boyut_sayisi}/1024")
    print(f"   Time: {result.hesaplama_suresi_ms:.2f}ms")
    
    # 6. Statistics
    print("\\n5. System statistics:")
    stats = system.istatistikler()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\\n" + "=" * 60)
    print("✓ Example completed successfully!")
 if __name__ == "__main__":
    main()
 """