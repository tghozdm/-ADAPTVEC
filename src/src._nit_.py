SRC_INIT = """\"\"\"
 AdaptVec: Word-Specific Dimension Selection for WSD
 Copyright (C) 2025 [tolgahan özdemir]
 License: CC BY-NC-ND 4.0
 \"\"\"
 from .core import HibritVektorSistemi, TahminSonucu
 from .optimizer import BoyutOptimizasyon
 __version__ = "1.0.0"
 __author__ = "[tolgahan .özdemir]"
 __license__ = "CC-BY-NC-ND-4.0"
__all__ = [
    "HibritVektorSistemi",
    "BoyutOptimizasyon", 
    "TahminSonucu"
 ]
 ""