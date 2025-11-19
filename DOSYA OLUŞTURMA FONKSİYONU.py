def dosyalari_olustur():
    """Create all files"""
    
    dosyalar = {
        'README.md': README_MD,
        'LICENSE': LICENSE,
        'requirements.txt': REQUIREMENTS,
        'setup.py': SETUP_PY,
        '.gitignore': GITIGNORE,
        'src/__init__.py': SRC_INIT,
        'src/core.py': SRC_CORE,
        'src/optimizer.py': SRC_OPTIMIZER,
        'src/utils.py': SRC_UTILS,
        'examples/basic_usage.py': EXAMPLES_BASIC,
    }
    
    print("="*70)
    print("ADAPTVEC - GITHUB REPOSITORY FILES")
    print("="*70)
    print("\\nFiles to create:\\n")
    
    for dosya_adi, icerik in dosyalar.items():
        lines = icerik.count('\\n')
        chars = len(icerik)
        print(f"
 📄
 {dosya_adi:30s} ({lines:4d} lines, {chars:6d} chars)")
    
    print("\\n" + "="*70)
    print("To create files, run:")
    print("="*70)
    print("""
 import os
 dosyalar = {
    'README.md': README_MD,
    'LICENSE': LICENSE,
    'requirements.txt': REQUIREMENTS,
    'setup.py': SETUP_PY,
    '.gitignore': GITIGNORE,
    'src/__init__.py': SRC_INIT,
    'src/core.py': SRC_CORE,
    'src/optimizer.py': SRC_OPTIMIZER,
    'src/utils.py': SRC_UTILS,
    'examples/basic_usage.py': EXAMPLES_BASIC,
 }
 for dosya, icerik in dosyalar.items():
    os.makedirs(os.path.dirname(dosya) if os.path.dirname(dosya) else '.', 
exist_ok=True)
    with open(dosya, 'w', encoding='utf-8') as f:
f.write(icerik)
 print(f"✓ Created: {dosya}")
 """)
 return dosyalar
 # Test
 if __name__ == "__main__":
 dosyalari_olustur()