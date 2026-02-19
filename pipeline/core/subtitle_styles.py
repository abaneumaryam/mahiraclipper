"""
MahiraClipper — Subtitle Style Presets
20+ preset style subtitle khusus konten dakwah & ceramah Islam.
Semua berbasis format ASS (Advanced SubStation Alpha) — no extra libs needed.

Cara pakai:
    from core.subtitle_styles import get_style, list_styles, STYLES
    style = get_style("hormozi_kuning")
"""

# ─── Format Warna ASS: &H{alpha}{B}{G}{R}& ────────────────────────────────────
# Alpha: 00=opaque, FF=transparent
# Contoh: putih opaque = &H00FFFFFF&

STYLES = {

    # ══════════════════════════════════════════════════════════════════
    # 1. HORMOZI KUNING — style paling viral, bold & tegas
    # ══════════════════════════════════════════════════════════════════
    "hormozi_kuning": {
        "name": "Hormozi Kuning",
        "desc": "Bold kuning terang, cocok untuk kutipan viral & nasihat tegas",
        "category_match": ["viral_quote", "knowledge"],
        "font": "Montserrat-Black",
        "base_size": 70,
        "highlight_size": 84,
        "base_color":      "&H00FFFFFF&",   # putih
        "highlight_color": "&H0000FFFF&",   # kuning
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 2.5,
        "outline_color":  "&HFF000000&",   # hitam
        "shadow_size": 0,
        "shadow_color":   "&H00000000&",
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 2. HORMOZI HIJAU — warna Islam, elegan & kuat
    # ══════════════════════════════════════════════════════════════════
    "hormozi_hijau": {
        "name": "Hormozi Hijau",
        "desc": "Bold hijau Islam, cocok untuk ayat/hadits & ilmu padat",
        "category_match": ["quran_hadith", "knowledge"],
        "font": "Montserrat-Black",
        "base_size": 70,
        "highlight_size": 84,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H0033CC00&",   # hijau Islam
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 2.5,
        "outline_color":  "&HFF000000&",
        "shadow_size": 0,
        "shadow_color":   "&H00000000&",
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 3. SOFT DAKWAH — hijau muda lembut, nuansa tenang & damai
    # ══════════════════════════════════════════════════════════════════
    "soft_dakwah": {
        "name": "Soft Dakwah",
        "desc": "Hijau mint lembut, cocok untuk konten emosional & menyentuh hati",
        "category_match": ["emotional", "beginner"],
        "font": "Poppins-SemiBold",
        "base_size": 64,
        "highlight_size": 76,
        "base_color":      "&H00F0F0F0&",   # putih susu
        "highlight_color": "&H0090EE90&",   # hijau mint
        "bold": 0,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 2.0,
        "outline_color":  "&HCC1A3A1A&",   # hijau tua transparan
        "shadow_size": 2,
        "shadow_color":   "&H88000000&",
        "mode": "highlight",
        "words_per_block": 4,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 4. CINEMA PUTIH — outline hitam tebal, clean & profesional
    # ══════════════════════════════════════════════════════════════════
    "cinema_putih": {
        "name": "Cinema Putih",
        "desc": "Putih bold outline hitam tebal, style film dokumenter",
        "category_match": ["knowledge", "quran_hadith"],
        "font": "Montserrat-Bold",
        "base_size": 68,
        "highlight_size": 82,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H00E0E0E0&",   # putih keabu
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 3.5,
        "outline_color":  "&HFF000000&",
        "shadow_size": 3,
        "shadow_color":   "&HAA000000&",
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 5. NEWS MERAH — tegas & dramatis, untuk peringatan keras
    # ══════════════════════════════════════════════════════════════════
    "news_merah": {
        "name": "News Merah",
        "desc": "Merah tegas ala berita, cocok untuk peringatan & momen emosional kuat",
        "category_match": ["emotional"],
        "font": "Montserrat-Black",
        "base_size": 68,
        "highlight_size": 82,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H000000FF&",   # merah
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 2.5,
        "outline_color":  "&HFF000000&",
        "shadow_size": 0,
        "shadow_color":   "&H00000000&",
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 6. BOX HITAM — teks di atas background box gelap, sangat terbaca
    # ══════════════════════════════════════════════════════════════════
    "box_hitam": {
        "name": "Box Hitam",
        "desc": "Background box hitam transparan, teks kuning — terbaca di background apapun",
        "category_match": ["viral_quote", "knowledge"],
        "font": "Montserrat-Bold",
        "base_size": 64,
        "highlight_size": 76,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H0000FFFF&",   # kuning
        "bold": 1,
        "italic": 0,
        "border_style": 3,                  # box mode
        "outline_thickness": 15,            # padding box
        "outline_color":  "&HAA000000&",   # hitam 67% transparan
        "shadow_size": 0,
        "shadow_color":   "&H00000000&",
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 7. BOX HIJAU ISLAM — box hijau gelap, nuansa resmi & islami
    # ══════════════════════════════════════════════════════════════════
    "box_hijau_islam": {
        "name": "Box Hijau Islam",
        "desc": "Box hijau tua dengan teks putih bold, nuansa kajian resmi",
        "category_match": ["quran_hadith", "knowledge"],
        "font": "Montserrat-Bold",
        "base_size": 64,
        "highlight_size": 76,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H0090EE90&",   # highlight hijau muda
        "bold": 1,
        "italic": 0,
        "border_style": 3,
        "outline_thickness": 15,
        "outline_color":  "&HAA1A5C1A&",   # hijau tua transparan
        "shadow_size": 0,
        "shadow_color":   "&H00000000&",
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 8. GLOW EMAS — golden glow, mewah & berkesan
    # ══════════════════════════════════════════════════════════════════
    "glow_emas": {
        "name": "Glow Emas",
        "desc": "Teks emas dengan glow effect, kesan mewah & berkesan untuk quote penting",
        "category_match": ["viral_quote", "quran_hadith"],
        "font": "Montserrat-Bold",
        "base_size": 68,
        "highlight_size": 82,
        "base_color":      "&H00D4D4D4&",   # abu terang
        "highlight_color": "&H0000D4FF&",   # emas
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 3.0,
        "outline_color":  "&HBB7A5200&",   # biru tua (jadi glow keemasan)
        "shadow_size": 4,
        "shadow_color":   "&H660064FF&",   # shadow emas redup
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 9. MINIMALIS PUTIH — bersih, tidak ramai, fokus ke konten
    # ══════════════════════════════════════════════════════════════════
    "minimalis_putih": {
        "name": "Minimalis Putih",
        "desc": "Clean & minimalis, cocok untuk ceramah yang butuh fokus ke wajah",
        "category_match": ["beginner", "knowledge"],
        "font": "Poppins-Regular",
        "base_size": 62,
        "highlight_size": 70,
        "base_color":      "&H00CCCCCC&",   # putih redup
        "highlight_color": "&H00FFFFFF&",   # putih penuh
        "bold": 0,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 1.5,
        "outline_color":  "&HDD000000&",
        "shadow_size": 1,
        "shadow_color":   "&H66000000&",
        "mode": "highlight",
        "words_per_block": 4,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": False,
    },

    # ══════════════════════════════════════════════════════════════════
    # 10. CYAN MODERN — segar & modern, cocok untuk pemuda
    # ══════════════════════════════════════════════════════════════════
    "cyan_modern": {
        "name": "Cyan Modern",
        "desc": "Cyan cerah, style modern & segar, cocok untuk audiens muda",
        "category_match": ["beginner", "viral_quote"],
        "font": "Montserrat-Bold",
        "base_size": 68,
        "highlight_size": 80,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H00FFFF00&",   # cyan
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 2.5,
        "outline_color":  "&HFF000000&",
        "shadow_size": 2,
        "shadow_color":   "&H88003333&",
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 11. WORD BY WORD KUNING — satu kata muncul satu-satu
    # ══════════════════════════════════════════════════════════════════
    "word_by_word_kuning": {
        "name": "Word by Word Kuning",
        "desc": "Setiap kata muncul satu per satu dengan highlight kuning",
        "category_match": ["viral_quote", "emotional"],
        "font": "Montserrat-Black",
        "base_size": 80,
        "highlight_size": 96,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H0000FFFF&",
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 3.0,
        "outline_color":  "&HFF000000&",
        "shadow_size": 0,
        "shadow_color":   "&H00000000&",
        "mode": "word_by_word",
        "words_per_block": 1,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 12. WORD BY WORD HIJAU — satu kata, warna Islam
    # ══════════════════════════════════════════════════════════════════
    "word_by_word_hijau": {
        "name": "Word by Word Hijau",
        "desc": "Kata per kata dengan highlight hijau Islam, dramatis & fokus",
        "category_match": ["quran_hadith", "emotional"],
        "font": "Montserrat-Black",
        "base_size": 80,
        "highlight_size": 96,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H0033CC00&",
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 3.0,
        "outline_color":  "&HFF000000&",
        "shadow_size": 0,
        "shadow_color":   "&H00000000&",
        "mode": "word_by_word",
        "words_per_block": 1,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 13. KARAOKE EMAS — semua teks muncul, highlight emas bergerak
    # ══════════════════════════════════════════════════════════════════
    "karaoke_emas": {
        "name": "Karaoke Emas",
        "desc": "Semua teks tampil sekaligus, kata aktif jadi emas — ala lirik lagu",
        "category_match": ["viral_quote", "quran_hadith"],
        "font": "Montserrat-Bold",
        "base_size": 64,
        "highlight_size": 76,
        "base_color":      "&H88AAAAAA&",   # abu transparan (sudah lewat)
        "highlight_color": "&H0000D4FF&",   # emas (sedang aktif)
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 2.0,
        "outline_color":  "&HFF000000&",
        "shadow_size": 2,
        "shadow_color":   "&H66000000&",
        "mode": "highlight",
        "words_per_block": 5,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 14. TEBAL BESAR — ukuran jumbo, cocok untuk quote singkat kuat
    # ══════════════════════════════════════════════════════════════════
    "tebal_besar": {
        "name": "Tebal Besar",
        "desc": "Font jumbo super bold, 1-2 kata per baris, maksimal impact visual",
        "category_match": ["viral_quote"],
        "font": "Montserrat-Black",
        "base_size": 96,
        "highlight_size": 116,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H0000FFFF&",   # kuning
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 4.0,
        "outline_color":  "&HFF000000&",
        "shadow_size": 0,
        "shadow_color":   "&H00000000&",
        "mode": "word_by_word",
        "words_per_block": 2,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 15. ITALIC ELEGAN — miring & halus, untuk nasihat lembut
    # ══════════════════════════════════════════════════════════════════
    "italic_elegan": {
        "name": "Italic Elegan",
        "desc": "Italic halus dengan highlight oranye, kesan elegan & bijaksana",
        "category_match": ["emotional", "beginner"],
        "font": "Poppins-SemiBoldItalic",
        "base_size": 64,
        "highlight_size": 76,
        "base_color":      "&H00E8E8E8&",
        "highlight_color": "&H000088FF&",   # oranye
        "bold": 0,
        "italic": 1,
        "border_style": 1,
        "outline_thickness": 2.0,
        "outline_color":  "&HDD000000&",
        "shadow_size": 3,
        "shadow_color":   "&H99000000&",
        "mode": "highlight",
        "words_per_block": 4,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": False,
    },

    # ══════════════════════════════════════════════════════════════════
    # 16. SHADOW DRAMATIS — shadow tebal tanpa outline, sinematik
    # ══════════════════════════════════════════════════════════════════
    "shadow_dramatis": {
        "name": "Shadow Dramatis",
        "desc": "Shadow tebal dramatis tanpa outline, kesan sinematik & mendalam",
        "category_match": ["emotional", "quran_hadith"],
        "font": "Montserrat-Bold",
        "base_size": 70,
        "highlight_size": 84,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H0090EE90&",   # hijau muda
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 0,
        "outline_color":  "&H00000000&",
        "shadow_size": 6,
        "shadow_color":   "&HCC000000&",    # shadow hitam kuat
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 17. UNDERLINE STYLE — underline pada kata aktif
    # ══════════════════════════════════════════════════════════════════
    "underline_bersih": {
        "name": "Underline Bersih",
        "desc": "Teks putih bersih, kata aktif di-underline — fokus tanpa gangguan warna",
        "category_match": ["knowledge", "beginner"],
        "font": "Poppins-SemiBold",
        "base_size": 64,
        "highlight_size": 70,
        "base_color":      "&H00DDDDDD&",
        "highlight_color": "&H00FFFFFF&",
        "bold": 0,
        "italic": 0,
        "underline": 1,
        "border_style": 1,
        "outline_thickness": 2.0,
        "outline_color":  "&HCC000000&",
        "shadow_size": 2,
        "shadow_color":   "&H66000000&",
        "mode": "highlight",
        "words_per_block": 4,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": False,
    },

    # ══════════════════════════════════════════════════════════════════
    # 18. DUALCOLOR UNGU — ungu & putih, modern & berbeda
    # ══════════════════════════════════════════════════════════════════
    "dualcolor_ungu": {
        "name": "Dualcolor Ungu",
        "desc": "Highlight ungu terang, tampil beda dari yang lain",
        "category_match": ["beginner", "viral_quote"],
        "font": "Montserrat-Bold",
        "base_size": 68,
        "highlight_size": 80,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H00FF44CC&",   # ungu/magenta
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 2.5,
        "outline_color":  "&HFF000000&",
        "shadow_size": 2,
        "shadow_color":   "&H88330033&",
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 19. NO HIGHLIGHT CLEAN — tanpa highlight, semua teks sama rata
    # ══════════════════════════════════════════════════════════════════
    "no_highlight_clean": {
        "name": "No Highlight Clean",
        "desc": "Tanpa highlight, teks putih bersih berganti per blok — simpel & rapi",
        "category_match": ["knowledge", "beginner"],
        "font": "Poppins-Regular",
        "base_size": 64,
        "highlight_size": 64,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H00FFFFFF&",
        "bold": 0,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 2.0,
        "outline_color":  "&HEE000000&",
        "shadow_size": 2,
        "shadow_color":   "&H77000000&",
        "mode": "no_highlight",
        "words_per_block": 5,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": False,
    },

    # ══════════════════════════════════════════════════════════════════
    # 20. ARABIC STYLE — font besar, cocok teks Arab + terjemah
    # ══════════════════════════════════════════════════════════════════
    "arabic_style": {
        "name": "Arabic Style",
        "desc": "Font lebih besar & tebal khusus teks Arab + terjemah Indonesia",
        "category_match": ["quran_hadith"],
        "font": "Scheherazade-Bold",
        "base_size": 76,
        "highlight_size": 90,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H0033CC00&",   # hijau
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 2.5,
        "outline_color":  "&HFF000000&",
        "shadow_size": 3,
        "shadow_color":   "&H88000000&",
        "mode": "highlight",
        "words_per_block": 2,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": False,
    },

    # ══════════════════════════════════════════════════════════════════
    # 21. FIRE ORANGE — oranye menyala, energi tinggi
    # ══════════════════════════════════════════════════════════════════
    "fire_orange": {
        "name": "Fire Orange",
        "desc": "Oranye menyala dengan shadow merah, energi tinggi untuk momen klimaks",
        "category_match": ["emotional", "viral_quote"],
        "font": "Montserrat-Black",
        "base_size": 70,
        "highlight_size": 84,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H000066FF&",   # oranye
        "bold": 1,
        "italic": 0,
        "border_style": 1,
        "outline_thickness": 2.5,
        "outline_color":  "&HFF000000&",
        "shadow_size": 3,
        "shadow_color":   "&H880000CC&",    # shadow merah
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # 22. PREMIUM DARK — teks di tengah layar gelap, ala quote card
    # ══════════════════════════════════════════════════════════════════
    "premium_dark": {
        "name": "Premium Dark",
        "desc": "Box gelap di tengah, teks besar putih — ala quote card Instagram",
        "category_match": ["viral_quote", "quran_hadith"],
        "font": "Montserrat-Bold",
        "base_size": 76,
        "highlight_size": 90,
        "base_color":      "&H00FFFFFF&",
        "highlight_color": "&H0000D4FF&",   # emas
        "bold": 1,
        "italic": 0,
        "border_style": 3,
        "outline_thickness": 20,
        "outline_color":  "&HCC000000&",    # box hitam
        "shadow_size": 0,
        "shadow_color":   "&H00000000&",
        "mode": "highlight",
        "words_per_block": 3,
        "vertical_position": 120,
        "alignment": 2,
        "remove_punctuation": True,
    },

    # ══════════════════════════════════════════════════════════════════
    # BATCH 2 & 3 — 50 Style Baru
    # ══════════════════════════════════════════════════════════════════

    # ─── NEON SERIES ────────────────────────────────────────────────
    "neon_pink": {"name":"Neon Pink","desc":"Merah jambu neon, anak muda","category_match":["viral_quote","beginner"],"font":"Montserrat-Black","base_size":70,"highlight_size":86,"base_color":"&H00FFFFFF&","highlight_color":"&H00FF44FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H88FF00FF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "neon_biru": {"name":"Neon Biru Elektrik","desc":"Biru elektrik futuristik","category_match":["viral_quote","beginner"],"font":"Montserrat-Black","base_size":70,"highlight_size":86,"base_color":"&H00FFFFFF&","highlight_color":"&H00FF8800&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H880088FF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "neon_hijau_gelap": {"name":"Neon Hijau Night","desc":"Hijau neon gelap, dramatic night mode","category_match":["viral_quote","emotional"],"font":"Montserrat-Black","base_size":70,"highlight_size":86,"base_color":"&H00AAAAAA&","highlight_color":"&H0000FF88&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":5,"shadow_color":"&H8800FF44&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "neon_oranye": {"name":"Neon Oranye Api","desc":"Oranye neon menyala, energi ekstrem","category_match":["viral_quote","emotional"],"font":"Montserrat-Black","base_size":72,"highlight_size":88,"base_color":"&H00FFFFFF&","highlight_color":"&H000055FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":4,"shadow_color":"&H770033FF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "neon_cyan_glow": {"name":"Neon Cyan Glow","desc":"Cyan glow terang, tampilan keren","category_match":["viral_quote","beginner"],"font":"Montserrat-Black","base_size":70,"highlight_size":84,"base_color":"&H00888888&","highlight_color":"&H00FFFF00&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":8,"shadow_color":"&H88FFFF00&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── BOX SERIES ─────────────────────────────────────────────────
    "box_merah": {"name":"Box Merah Peringatan","desc":"Box merah tua, peringatan penting","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":68,"highlight_size":82,"base_color":"&H00FFFFFF&","highlight_color":"&H0044AAFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC0000CC&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "box_emas": {"name":"Box Emas Mewah","desc":"Box emas mewah, ayat & hadits istimewa","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Bold","base_size":66,"highlight_size":80,"base_color":"&H00FFFFFF&","highlight_color":"&H0000D4FF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC1E3A6E&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "box_ungu": {"name":"Box Ungu Elegan","desc":"Box ungu gelap, elegan dan beda","category_match":["emotional","beginner"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H00FFFFFF&","highlight_color":"&H00FF88FF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC4B0082&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "box_putih": {"name":"Box Putih Bersih","desc":"Box putih teks gelap, elegant","category_match":["knowledge","beginner"],"font":"Montserrat-SemiBold","base_size":64,"highlight_size":78,"base_color":"&H00333333&","highlight_color":"&H002D6B42&","bold":0,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCCF5F5F5&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "box_transparan": {"name":"Box Semi-Transparan","desc":"Box hitam transparan, clean & modern","category_match":["knowledge","viral_quote"],"font":"Poppins-SemiBold","base_size":66,"highlight_size":80,"base_color":"&H00FFFFFF&","highlight_color":"&H0000FFFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HAA000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "box_biru_tua": {"name":"Box Biru Navy","desc":"Box navy profesional, serius & akademis","category_match":["knowledge","quran_hadith"],"font":"Montserrat-Bold","base_size":66,"highlight_size":80,"base_color":"&H00FFFFFF&","highlight_color":"&H00FFCC88&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC000033&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── WORD-BY-WORD SERIES ─────────────────────────────────────────
    "wbw_merah": {"name":"Word×Word Merah Api","desc":"Kata per kata merah, tegas & keras","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":82,"highlight_size":98,"base_color":"&H00FFFFFF&","highlight_color":"&H000000FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H660000FF&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "wbw_emas": {"name":"Word×Word Emas","desc":"Kata per kata emas berkilau, sangat impactful","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Black","base_size":82,"highlight_size":98,"base_color":"&H00CCCCCC&","highlight_color":"&H0000D4FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":4,"shadow_color":"&H440088FF&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "wbw_ungu": {"name":"Word×Word Ungu","desc":"Kata per kata ungu, misterius & mendalam","category_match":["emotional","beginner"],"font":"Montserrat-Black","base_size":82,"highlight_size":98,"base_color":"&H00FFFFFF&","highlight_color":"&H00FF44FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H66FF00FF&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "wbw_putih_xl": {"name":"Word×Word Putih XL","desc":"Putih jumbo satu kata, maksimal impak","category_match":["viral_quote","emotional"],"font":"Montserrat-Black","base_size":90,"highlight_size":108,"base_color":"&H00DDDDDD&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":4.5,"outline_color":"&HFF000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "wbw_cyan": {"name":"Word×Word Cyan","desc":"Cyan satu kata, fresh & energik","category_match":["beginner","viral_quote"],"font":"Montserrat-Black","base_size":82,"highlight_size":98,"base_color":"&H00FFFFFF&","highlight_color":"&H00FFFF00&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44FFFF00&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "wbw_hijau_tua": {"name":"Word×Word Hijau Islam","desc":"Hijau tua per kata, khusus kajian Islam","category_match":["quran_hadith","knowledge"],"font":"Montserrat-Black","base_size":82,"highlight_size":98,"base_color":"&H00AAAAAA&","highlight_color":"&H0033CC00&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44006600&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "wbw_box_hitam": {"name":"Word×Word Box Hitam","desc":"Satu kata per box hitam, paling dramatis","category_match":["viral_quote","emotional"],"font":"Montserrat-Black","base_size":82,"highlight_size":98,"base_color":"&H00FFFFFF&","highlight_color":"&H0000FFFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HDD000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── KARAOKE SERIES ──────────────────────────────────────────────
    "karaoke_hijau": {"name":"Karaoke Hijau Islam","desc":"Abu jadi hijau saat aktif, seperti lirik","category_match":["quran_hadith","knowledge"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H88AAAAAA&","highlight_color":"&H0033CC00&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44006600&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "karaoke_merah": {"name":"Karaoke Merah Dramatis","desc":"Abu jadi merah aktif, sangat dramatis","category_match":["emotional","viral_quote"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H88AAAAAA&","highlight_color":"&H000000FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44FF0000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "karaoke_putih": {"name":"Karaoke Putih Bersih","desc":"Gelap ke putih terang, profesional","category_match":["knowledge","beginner"],"font":"Poppins-SemiBold","base_size":66,"highlight_size":80,"base_color":"&H66888888&","highlight_color":"&H00FFFFFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":1.8,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "karaoke_emas_2": {"name":"Karaoke Emas Premium","desc":"Versi premium karaoke emas berkilap","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Bold","base_size":68,"highlight_size":84,"base_color":"&H66999988&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44004488&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── BLOK KATA SERIES ────────────────────────────────────────────
    "blok_2kata": {"name":"Blok 2 Kata Dramatis","desc":"2 kata besar, super fokus & impactful","category_match":["viral_quote","emotional"],"font":"Montserrat-Black","base_size":84,"highlight_size":100,"base_color":"&H00DDDDDD&","highlight_color":"&H0000FFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.5,"outline_color":"&HFF000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":2,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "blok_5kata": {"name":"Blok 5 Kata","desc":"5 kata sekaligus, ceramah cepat tetap kebaca","category_match":["knowledge","beginner"],"font":"Montserrat-Bold","base_size":62,"highlight_size":76,"base_color":"&H00FFFFFF&","highlight_color":"&H0000FFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":5,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "blok_6kata": {"name":"Blok 6 Kata Natural","desc":"6 kata, terasa seperti subtitle film","category_match":["knowledge","beginner"],"font":"Poppins-SemiBold","base_size":58,"highlight_size":70,"base_color":"&H00FFFFFF&","highlight_color":"&H0033CC00&","bold":0,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":6,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── GLOW SERIES ─────────────────────────────────────────────────
    "glow_putih": {"name":"Glow Putih Soft","desc":"Glow putih lembut, bersih & profesional","category_match":["knowledge","beginner"],"font":"Poppins-SemiBold","base_size":68,"highlight_size":82,"base_color":"&H00CCCCCC&","highlight_color":"&H00FFFFFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":7,"shadow_color":"&H66FFFFFF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "glow_hijau": {"name":"Glow Hijau Islami","desc":"Glow hijau zamrud, spiritual & islami","category_match":["quran_hadith","emotional"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H00AAAAAA&","highlight_color":"&H0033CC00&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":7,"shadow_color":"&H5500AA00&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "glow_merah": {"name":"Glow Merah Api","desc":"Glow merah berapi, emosional keras","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":70,"highlight_size":84,"base_color":"&H00AAAAAA&","highlight_color":"&H000000FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":8,"shadow_color":"&H550000FF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "glow_biru": {"name":"Glow Biru Dingin","desc":"Glow biru, tenang & intelektual","category_match":["knowledge","beginner"],"font":"Poppins-SemiBold","base_size":68,"highlight_size":82,"base_color":"&H00AAAAAA&","highlight_color":"&H00FF8800&","bold":0,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":7,"shadow_color":"&H55FF4400&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "glow_emas_2": {"name":"Glow Emas Double","desc":"Emas dengan glow dobel, paling mewah","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Black","base_size":72,"highlight_size":88,"base_color":"&H00BBAA88&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":9,"shadow_color":"&H550066AA&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── OUTLINE SERIES ──────────────────────────────────────────────
    "outline_sangat_tebal": {"name":"Outline Sangat Tebal","desc":"Outline 5px, terbaca di background apapun","category_match":["knowledge","viral_quote"],"font":"Montserrat-Black","base_size":70,"highlight_size":84,"base_color":"&H00FFFFFF&","highlight_color":"&H0000FFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":5.0,"outline_color":"&HFF000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "outline_hijau": {"name":"Outline Hijau Islam","desc":"Outline hijau Islam, unik & khas","category_match":["quran_hadith","knowledge"],"font":"Montserrat-Bold","base_size":70,"highlight_size":84,"base_color":"&H00FFFFFF&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.5,"outline_color":"&HFF006600&","shadow_size":2,"shadow_color":"&H44006600&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "outline_emas": {"name":"Outline Emas Premium","desc":"Outline emas, terasa premium & mewah","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Black","base_size":70,"highlight_size":84,"base_color":"&H00FFFFFF&","highlight_color":"&H0000D4FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.5,"outline_color":"&HFF1E3A6E&","shadow_size":3,"shadow_color":"&H441E3A6E&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "outline_merah": {"name":"Outline Merah Tegas","desc":"Outline merah, peringatan keras","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":70,"highlight_size":84,"base_color":"&H00FFFFFF&","highlight_color":"&H000000FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.5,"outline_color":"&HFF0000CC&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── POSISI TENGAH & ATAS ────────────────────────────────────────
    "tengah_putih": {"name":"Tengah Sinema Putih","desc":"Subtitle tengah layar, ala film sinema","category_match":["emotional","quran_hadith"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H00CCCCCC&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":4,"shadow_color":"&H66000000&","mode":"highlight","words_per_block":3,"vertical_position":900,"alignment":2,"remove_punctuation":True},
    "tengah_emas_sinema": {"name":"Tengah Emas Epik","desc":"Emas di tengah, ala film Islam epik","category_match":["quran_hadith","emotional"],"font":"Montserrat-Black","base_size":72,"highlight_size":86,"base_color":"&H00AAAAAA&","highlight_color":"&H0000D4FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":5,"shadow_color":"&H440088FF&","mode":"highlight","words_per_block":3,"vertical_position":900,"alignment":2,"remove_punctuation":True},
    "atas_putih": {"name":"Atas Layar Putih","desc":"Subtitle di atas, cocok wajah di bawah","category_match":["knowledge","beginner"],"font":"Montserrat-Bold","base_size":66,"highlight_size":80,"base_color":"&H00DDDDDD&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":3,"vertical_position":1700,"alignment":2,"remove_punctuation":True},
    "atas_kuning": {"name":"Atas Layar Kuning","desc":"Hormozi kuning di atas, beda & viral","category_match":["viral_quote","knowledge"],"font":"Montserrat-Black","base_size":68,"highlight_size":84,"base_color":"&H00FFFFFF&","highlight_color":"&H0000FFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":1700,"alignment":2,"remove_punctuation":True},

    # ─── CINEMATIC SERIES ────────────────────────────────────────────
    "cinematic_hitam": {"name":"Cinematic Box Hitam","desc":"Putih di box hitam penuh, ala dokumenter","category_match":["emotional","quran_hadith"],"font":"Montserrat-Bold","base_size":66,"highlight_size":80,"base_color":"&H00CCCCCC&","highlight_color":"&H00FFFFFF&","bold":0,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HDD000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "cinematic_subtitle": {"name":"Cinematic Film Subtitle","desc":"Gaya subtitle bioskop, italic tipis","category_match":["knowledge","emotional"],"font":"Poppins-Regular","base_size":56,"highlight_size":68,"base_color":"&H00FFFFFF&","highlight_color":"&H00FFFF88&","bold":0,"italic":1,"border_style":1,"outline_thickness":1.5,"outline_color":"&HFF000000&","shadow_size":1,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":6,"vertical_position":80,"alignment":2,"remove_punctuation":False},
    "cinematic_sepia": {"name":"Cinematic Sepia Klasik","desc":"Sepia hangat, kesan klasik & nostalgia","category_match":["emotional","quran_hadith"],"font":"Poppins-SemiBold","base_size":64,"highlight_size":78,"base_color":"&H00BBDDFF&","highlight_color":"&H0088CCFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},

    # ─── QURAN / ISLAMI SERIES ───────────────────────────────────────
    "quran_emas_besar": {"name":"Quran Emas Besar","desc":"Emas jumbo untuk ayat Al-Quran & hadits","category_match":["quran_hadith"],"font":"Montserrat-Black","base_size":76,"highlight_size":92,"base_color":"&H00CCCCAA&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":4,"shadow_color":"&H440066AA&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "quran_hijau_zamrud": {"name":"Quran Hijau Zamrud","desc":"Hijau zamrud mewah, kajian kitab","category_match":["quran_hadith","knowledge"],"font":"Montserrat-Bold","base_size":70,"highlight_size":84,"base_color":"&H00AACCAA&","highlight_color":"&H0022DD44&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44006622&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "quran_putih_biru": {"name":"Quran Putih-Biru Suci","desc":"Putih ke biru langit, suci & damai","category_match":["quran_hadith","emotional"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H00DDDDFF&","highlight_color":"&H00FFCCAA&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44AAAAFF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "hadits_tegas": {"name":"Hadits Tegas H-P","desc":"Bold bersih khusus hadits, hitam-putih","category_match":["quran_hadith","knowledge"],"font":"Montserrat-Black","base_size":70,"highlight_size":84,"base_color":"&H00EEEEEE&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC222222&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── PLATFORM & VLOG SERIES ──────────────────────────────────────
    "tiktok_trendy": {"name":"TikTok Trendy 2025","desc":"Style paling viral di TikTok, WxW kuning","category_match":["viral_quote","beginner"],"font":"Montserrat-Black","base_size":76,"highlight_size":92,"base_color":"&H00FFFFFF&","highlight_color":"&H00FFFF00&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "reels_modern": {"name":"Instagram Reels Modern","desc":"Clean modern ala konten Instagram terbaik","category_match":["viral_quote","beginner"],"font":"Poppins-SemiBold","base_size":68,"highlight_size":82,"base_color":"&H00FFFFFF&","highlight_color":"&H00FF88FF&","bold":0,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "shorts_bold": {"name":"YouTube Shorts Bold","desc":"Optimized untuk YouTube Shorts, bold max","category_match":["viral_quote","knowledge"],"font":"Montserrat-Black","base_size":76,"highlight_size":92,"base_color":"&H00FFFFFF&","highlight_color":"&H000000FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.5,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":3,"vertical_position":100,"alignment":2,"remove_punctuation":True},
    "vlog_kuning": {"name":"Vlog Kuning Ceria","desc":"Casual kuning, konten edukatif santai","category_match":["beginner","viral_quote"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H00FFFFFF&","highlight_color":"&H0000EEFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF333300&","shadow_size":2,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "vlog_pink": {"name":"Vlog Pink Remaja","desc":"Pink manis, konten muda & relatable","category_match":["beginner","emotional"],"font":"Poppins-SemiBold","base_size":66,"highlight_size":80,"base_color":"&H00FFFFFF&","highlight_color":"&H00CC44FF&","bold":0,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF330033&","shadow_size":2,"shadow_color":"&H44AA00AA&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "vlog_oranye": {"name":"Vlog Oranye Hangat","desc":"Oranye cerah, hangat & ramah","category_match":["beginner","emotional"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H00FFFFFF&","highlight_color":"&H000055FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF331100&","shadow_size":2,"shadow_color":"&H44FF4400&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── SPECIAL / UNIK SERIES ───────────────────────────────────────
    "minimalis_tipis": {"name":"Minimalis Tipis Elegan","desc":"Font tipis tidak bold, elegan & dewasa","category_match":["knowledge","beginner"],"font":"Poppins-Regular","base_size":60,"highlight_size":72,"base_color":"&H00DDDDDD&","highlight_color":"&H00FFFFFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":1.5,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":5,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "minimalis_cream": {"name":"Minimalis Cream Hangat","desc":"Cream warm tone, nyaman di mata","category_match":["knowledge","emotional"],"font":"Poppins-SemiBold","base_size":64,"highlight_size":78,"base_color":"&H00BBCCEE&","highlight_color":"&H00DDEEFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":1.5,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H33000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "military_green": {"name":"Military Green","desc":"Hijau tua military, gagah & berkarakter","category_match":["knowledge","viral_quote"],"font":"Montserrat-Black","base_size":70,"highlight_size":84,"base_color":"&H00AABBAA&","highlight_color":"&H0044AA44&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44224422&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "typewriter": {"name":"Typewriter Klasik","desc":"Gaya mesin ketik, satu kata per tampil","category_match":["knowledge","viral_quote"],"font":"Poppins-Regular","base_size":64,"highlight_size":78,"base_color":"&H00DDDDDD&","highlight_color":"&H00FFFFFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":1.5,"outline_color":"&HFF000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "dakwah_bijak": {"name":"Dakwah Bijak Italic","desc":"Italic elegan emas, nasihat & hikmah","category_match":["emotional","quran_hadith"],"font":"Poppins-SemiBold","base_size":64,"highlight_size":78,"base_color":"&H00DDDDAA&","highlight_color":"&H0000CCFF&","bold":0,"italic":1,"border_style":1,"outline_thickness":1.5,"outline_color":"&HFF000000&","shadow_size":4,"shadow_color":"&H440066AA&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "motivasi_merah": {"name":"Motivasi Merah Membara","desc":"Merah per kata, momen motivasi keras","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":76,"highlight_size":92,"base_color":"&H00FFFFFF&","highlight_color":"&H002222FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H553333FF&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "tausiyah_lembut": {"name":"Tausiyah Lembut","desc":"Hijau muda italic, nasehat hati","category_match":["emotional","beginner"],"font":"Poppins-SemiBold","base_size":64,"highlight_size":78,"base_color":"&H00CCEECC&","highlight_color":"&H0088FF88&","bold":0,"italic":1,"border_style":1,"outline_thickness":1.5,"outline_color":"&HFF003300&","shadow_size":3,"shadow_color":"&H33006600&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "podcast_clean": {"name":"Podcast Clean 5-Kata","desc":"Bersih 5 kata, ideal ceramah panjang","category_match":["knowledge","beginner"],"font":"Poppins-SemiBold","base_size":60,"highlight_size":74,"base_color":"&H00FFFFFF&","highlight_color":"&H0066FFFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":5,"vertical_position":100,"alignment":2,"remove_punctuation":False},
    "podcast_dark": {"name":"Podcast Dark Mode","desc":"Gelap elegan, konten malam hari","category_match":["knowledge","emotional"],"font":"Poppins-SemiBold","base_size":62,"highlight_size":76,"base_color":"&H00888888&","highlight_color":"&H00CCCCCC&","bold":0,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC111111&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":5,"vertical_position":100,"alignment":2,"remove_punctuation":False},
    "futuristik_dark": {"name":"Futuristik Dark","desc":"Latar gelap transparan, teks cyan futuristik","category_match":["viral_quote","beginner"],"font":"Montserrat-Black","base_size":68,"highlight_size":84,"base_color":"&H00888888&","highlight_color":"&H00EEFF00&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HAA000000&","shadow_size":5,"shadow_color":"&H55EEFF00&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "elegan_emas_italic": {"name":"Elegan Emas Italic","desc":"Italic emas tipis, paling elegan & premium","category_match":["quran_hadith","emotional"],"font":"Poppins-Regular","base_size":62,"highlight_size":76,"base_color":"&H00AABB88&","highlight_color":"&H0000CCFF&","bold":0,"italic":1,"border_style":1,"outline_thickness":1.5,"outline_color":"&HFF000000&","shadow_size":5,"shadow_color":"&H440066AA&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "bold_putih_polos": {"name":"Bold Putih Polos","desc":"Putih bold tanpa efek, simpel & kuat","category_match":["knowledge","viral_quote"],"font":"Montserrat-Black","base_size":72,"highlight_size":88,"base_color":"&H00FFFFFF&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"no_highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "hijau_kontras_max": {"name":"Hijau-Putih Kontras Max","desc":"Kontras maksimal, paling mudah dibaca","category_match":["knowledge","quran_hadith"],"font":"Montserrat-Black","base_size":70,"highlight_size":84,"base_color":"&H00FFFFFF&","highlight_color":"&H0000BB00&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF003300&","shadow_size":2,"shadow_color":"&H44003300&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "shadow_biru": {"name":"Shadow Biru Dramatis","desc":"Shadow biru tebal, dingin & mendalam","category_match":["emotional","knowledge"],"font":"Montserrat-Bold","base_size":70,"highlight_size":84,"base_color":"&H00FFFFFF&","highlight_color":"&H00FF8800&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":7,"shadow_color":"&H55FF4400&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "retro_vintage": {"name":"Retro Vintage","desc":"Kuning tua retro, klasik & berkarakter","category_match":["viral_quote","beginner"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H00AAAAFF&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF111100&","shadow_size":3,"shadow_color":"&H55003388&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ══════════════════════════════════════════════════════════════════
    # BATCH 4 — 50 Style Baru (Grand Total 138)
    # ══════════════════════════════════════════════════════════════════

    # ─── GRADIENT WARNA SERIES ───────────────────────────────────────
    "gradient_merah_kuning": {"name":"Gradient Merah-Kuning","desc":"Panas membara, urgensi & peringatan keras","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":72,"highlight_size":88,"base_color":"&H0000AAFF&","highlight_color":"&H000000FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H55000088&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "gradient_biru_ungu": {"name":"Gradient Biru-Ungu","desc":"Elegan cool, konten modern premium","category_match":["viral_quote","beginner"],"font":"Montserrat-Black","base_size":70,"highlight_size":86,"base_color":"&H00FFAAFF&","highlight_color":"&H00FF4444&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":4,"shadow_color":"&H55FF00AA&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "gradient_hijau_teal": {"name":"Gradient Hijau-Teal","desc":"Segar & natural, konten Islami muda","category_match":["quran_hadith","beginner"],"font":"Montserrat-Bold","base_size":70,"highlight_size":84,"base_color":"&H00DDFFDD&","highlight_color":"&H0000FF88&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H4400AA44&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "gold_silver": {"name":"Gold & Silver","desc":"Emas dan perak bergantian, super mewah","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Black","base_size":72,"highlight_size":88,"base_color":"&H00CCCCCC&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF111100&","shadow_size":5,"shadow_color":"&H440066AA&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── DUAL TONE SERIES ────────────────────────────────────────────
    "dual_hijau_putih": {"name":"Dual Hijau-Putih","desc":"Hijau & putih kontras tinggi, clean Islam","category_match":["quran_hadith","knowledge"],"font":"Montserrat-Black","base_size":70,"highlight_size":84,"base_color":"&H0099FF99&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF003300&","shadow_size":2,"shadow_color":"&H44006600&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "dual_merah_putih": {"name":"Dual Merah-Putih","desc":"Merah & putih kontras, tegas & menarik","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":70,"highlight_size":84,"base_color":"&H00FF9999&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF330000&","shadow_size":2,"shadow_color":"&H44880000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "dual_emas_hitam": {"name":"Dual Emas-Hitam","desc":"Emas di hitam, paling elegan & premium","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Black","base_size":72,"highlight_size":88,"base_color":"&H00888866&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":6,"shadow_color":"&H880066AA&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "dual_cyan_hitam": {"name":"Dual Cyan-Hitam","desc":"Cyan cerah di gelap, hacker aesthetic","category_match":["viral_quote","beginner"],"font":"Montserrat-Black","base_size":70,"highlight_size":86,"base_color":"&H00888888&","highlight_color":"&H00FFFF00&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HAA000000&","shadow_size":6,"shadow_color":"&H66FFFF00&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── SHADOW EKSTREM SERIES ───────────────────────────────────────
    "shadow_emas_tebal": {"name":"Shadow Emas Tebal","desc":"Shadow emas sangat tebal, mewah & dalam","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Black","base_size":72,"highlight_size":88,"base_color":"&H00DDDDAA&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":10,"shadow_color":"&H660066AA&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "shadow_hijau_deep": {"name":"Shadow Hijau Deep","desc":"Shadow hijau dalam, spiritual & syahdu","category_match":["quran_hadith","emotional"],"font":"Montserrat-Bold","base_size":70,"highlight_size":84,"base_color":"&H00AAAAAA&","highlight_color":"&H0033CC00&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":9,"shadow_color":"&H55006600&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "shadow_merah_inferno": {"name":"Shadow Merah Inferno","desc":"Shadow merah api, paling dramatis","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":74,"highlight_size":90,"base_color":"&H00CCCCCC&","highlight_color":"&H000000FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":10,"shadow_color":"&H660000FF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "shadow_ungu_mystic": {"name":"Shadow Ungu Mystic","desc":"Shadow ungu misterius, seperti sihir","category_match":["emotional","beginner"],"font":"Montserrat-Black","base_size":70,"highlight_size":86,"base_color":"&H00DDDDFF&","highlight_color":"&H00FF88FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":9,"shadow_color":"&H66FF00FF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── BOX ADVANCED SERIES ─────────────────────────────────────────
    "box_hijau_neon": {"name":"Box Hijau Neon","desc":"Box hijau neon gelap, unik & khas","category_match":["viral_quote","quran_hadith"],"font":"Montserrat-Black","base_size":68,"highlight_size":82,"base_color":"&H00AAFFAA&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC003300&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "box_oranye": {"name":"Box Oranye Energik","desc":"Box oranye muda, ceria & menarik","category_match":["beginner","viral_quote"],"font":"Montserrat-Bold","base_size":66,"highlight_size":80,"base_color":"&H00FFFFFF&","highlight_color":"&H000055FF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC331100&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "box_abu_gelap": {"name":"Box Abu Gelap","desc":"Box abu gelap, clean dark mode","category_match":["knowledge","emotional"],"font":"Poppins-SemiBold","base_size":64,"highlight_size":78,"base_color":"&H00CCCCCC&","highlight_color":"&H00FFFFFF&","bold":0,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC333333&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "box_merah_neon": {"name":"Box Merah Neon","desc":"Box merah neon gelap, sangat mencolok","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":68,"highlight_size":84,"base_color":"&H00FFFFFF&","highlight_color":"&H0000FFFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC880000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "box_ungu_royal": {"name":"Box Ungu Royal","desc":"Box ungu kerajaan, paling mewah","category_match":["quran_hadith","emotional"],"font":"Montserrat-Bold","base_size":66,"highlight_size":80,"base_color":"&H00FFDDFF&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC220044&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── MULTI KATA EKSTREM SERIES ───────────────────────────────────
    "satu_kata_raksasa": {"name":"1 Kata Raksasa","desc":"Satu kata sangat besar, ultra dramatis","category_match":["viral_quote","emotional"],"font":"Montserrat-Black","base_size":100,"highlight_size":120,"base_color":"&H00DDDDDD&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":5.0,"outline_color":"&HFF000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "dua_kata_kotak": {"name":"2 Kata + Box Hitam","desc":"2 kata di box hitam, sangat bold","category_match":["viral_quote","emotional"],"font":"Montserrat-Black","base_size":82,"highlight_size":98,"base_color":"&H00FFFFFF&","highlight_color":"&H0000FFFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HDD000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":2,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "tujuh_kata": {"name":"7 Kata Per Baris","desc":"7 kata, sangat alami seperti baca teks","category_match":["knowledge","beginner"],"font":"Poppins-Regular","base_size":54,"highlight_size":66,"base_color":"&H00FFFFFF&","highlight_color":"&H0066FFFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":1.8,"outline_color":"&HFF000000&","shadow_size":1,"shadow_color":"&H33000000&","mode":"highlight","words_per_block":7,"vertical_position":100,"alignment":2,"remove_punctuation":False},

    # ─── ITALIC SERIES ───────────────────────────────────────────────
    "italic_putih": {"name":"Italic Putih Bersih","desc":"Italic putih bersih, gaya narasi film","category_match":["emotional","knowledge"],"font":"Poppins-SemiBold","base_size":66,"highlight_size":80,"base_color":"&H00DDDDDD&","highlight_color":"&H00FFFFFF&","bold":0,"italic":1,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "italic_emas": {"name":"Italic Emas Mewah","desc":"Italic emas, paling mewah untuk nasihat","category_match":["quran_hadith","emotional"],"font":"Poppins-SemiBold","base_size":66,"highlight_size":80,"base_color":"&H00AABB88&","highlight_color":"&H0000CCFF&","bold":0,"italic":1,"border_style":1,"outline_thickness":1.8,"outline_color":"&HFF000000&","shadow_size":5,"shadow_color":"&H44004488&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "italic_hijau": {"name":"Italic Hijau Damai","desc":"Italic hijau, damai & menenangkan","category_match":["quran_hadith","beginner"],"font":"Poppins-SemiBold","base_size":64,"highlight_size":78,"base_color":"&H00AACCAA&","highlight_color":"&H0055EE55&","bold":0,"italic":1,"border_style":1,"outline_thickness":1.8,"outline_color":"&HFF003300&","shadow_size":3,"shadow_color":"&H33006600&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "italic_merah": {"name":"Italic Merah Tegas","desc":"Italic merah, peringatan tapi elegan","category_match":["emotional","viral_quote"],"font":"Poppins-SemiBold","base_size":66,"highlight_size":80,"base_color":"&H00FFCCCC&","highlight_color":"&H000000FF&","bold":0,"italic":1,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF330000&","shadow_size":3,"shadow_color":"&H44FF0000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},

    # ─── POSISI KANAN/KIRI SERIES ────────────────────────────────────
    "kiri_putih": {"name":"Rata Kiri Putih","desc":"Teks rata kiri, gaya berita & dokumenter","category_match":["knowledge","emotional"],"font":"Montserrat-Bold","base_size":66,"highlight_size":80,"base_color":"&H00DDDDDD&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":1,"remove_punctuation":True},
    "kiri_kuning": {"name":"Rata Kiri Kuning","desc":"Hormozi kuning rata kiri, unik & viral","category_match":["viral_quote","knowledge"],"font":"Montserrat-Black","base_size":68,"highlight_size":84,"base_color":"&H00FFFFFF&","highlight_color":"&H0000FFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":1,"remove_punctuation":True},

    # ─── BACKGROUND BLUR/FROSTED SERIES ─────────────────────────────
    "frosted_putih": {"name":"Frosted Glass Putih","desc":"Efek kaca buram putih, sangat modern","category_match":["beginner","knowledge"],"font":"Poppins-SemiBold","base_size":64,"highlight_size":78,"base_color":"&H00444444&","highlight_color":"&H00111111&","bold":0,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCCEEEEFF&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "frosted_gelap": {"name":"Frosted Glass Gelap","desc":"Efek kaca gelap, konten premium malam","category_match":["knowledge","emotional"],"font":"Poppins-SemiBold","base_size":64,"highlight_size":78,"base_color":"&H00BBBBBB&","highlight_color":"&H00FFFFFF&","bold":0,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC111122&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},

    # ─── WBW ADVANCED SERIES ─────────────────────────────────────────
    "wbw_box_emas": {"name":"Word×Word Box Emas","desc":"Satu kata per box emas, sangat mewah","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Black","base_size":82,"highlight_size":98,"base_color":"&H00CCCCAA&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HDD1E3A6E&","shadow_size":0,"shadow_color":"&H00000000&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "wbw_box_merah": {"name":"Word×Word Box Merah","desc":"Satu kata per box merah, dramatis total","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":82,"highlight_size":98,"base_color":"&H00FFFFFF&","highlight_color":"&H000000FF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HDD880000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "wbw_neon_kuning": {"name":"Word×Word Neon Kuning","desc":"Satu kata neon kuning, paling mencolok","category_match":["viral_quote","beginner"],"font":"Montserrat-Black","base_size":84,"highlight_size":102,"base_color":"&H00888888&","highlight_color":"&H00FFFF00&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":7,"shadow_color":"&H66FFFF00&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "wbw_glow_putih": {"name":"Word×Word Glow Putih","desc":"Satu kata dengan glow putih intens","category_match":["emotional","viral_quote"],"font":"Montserrat-Black","base_size":84,"highlight_size":102,"base_color":"&H00AAAAAA&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":10,"shadow_color":"&H88FFFFFF&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── DESAIN ISLAMI KHUSUS ────────────────────────────────────────
    "subhanallah": {"name":"Subhanallah Style","desc":"Putih suci bercahaya, untuk dzikir & tasbih","category_match":["quran_hadith","emotional"],"font":"Montserrat-Bold","base_size":74,"highlight_size":90,"base_color":"&H00DDDDFF&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":7,"shadow_color":"&H66FFFFFF&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "asmaul_husna": {"name":"Asmaul Husna","desc":"Emas mulia, untuk penyebutan nama Allah","category_match":["quran_hadith"],"font":"Montserrat-Black","base_size":76,"highlight_size":92,"base_color":"&H00CCBB88&","highlight_color":"&H0000EEFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":5,"shadow_color":"&H4400AAFF&","mode":"word_by_word","words_per_block":1,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "khutbah_jumat": {"name":"Khutbah Jumat","desc":"Hitam putih tegas, khusus konten khutbah","category_match":["quran_hadith","knowledge"],"font":"Montserrat-Black","base_size":68,"highlight_size":82,"base_color":"&H00EEEEEE&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC111111&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "ramadan_emas": {"name":"Ramadan Emas","desc":"Emas festif untuk konten Ramadan & Eid","category_match":["quran_hadith","emotional"],"font":"Montserrat-Black","base_size":72,"highlight_size":88,"base_color":"&H00CCBB88&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":5,"shadow_color":"&H440066AA&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "hijriyah_perak": {"name":"Hijriyah Perak","desc":"Perak elegan, kalender Hijriyah & sejarah Islam","category_match":["quran_hadith","knowledge"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H00AAAAAA&","highlight_color":"&H00DDDDDD&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":4,"shadow_color":"&H44AAAAAA&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── PLATFORM ADVANCED ───────────────────────────────────────────
    "youtube_end_screen": {"name":"YouTube End Screen","desc":"Bold besar untuk intro/outro YouTube","category_match":["viral_quote","knowledge"],"font":"Montserrat-Black","base_size":80,"highlight_size":96,"base_color":"&H00FFFFFF&","highlight_color":"&H000000FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":4.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":2,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "instagram_story": {"name":"Instagram Story","desc":"Minimalis cantik, cocok Instagram Story","category_match":["beginner","emotional"],"font":"Poppins-SemiBold","base_size":66,"highlight_size":80,"base_color":"&H00FFFFFF&","highlight_color":"&H00FF66BB&","bold":0,"italic":0,"border_style":1,"outline_thickness":1.8,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "facebook_dakwah": {"name":"Facebook Dakwah","desc":"Besar & jelas, optimal untuk Facebook viewer tua","category_match":["knowledge","quran_hadith"],"font":"Montserrat-Bold","base_size":74,"highlight_size":90,"base_color":"&H00FFFFFF&","highlight_color":"&H0033CC00&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44000000&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "twitter_x_bold": {"name":"Twitter/X Bold","desc":"Tajam & ringkas, gaya Twitter/X post","category_match":["viral_quote","knowledge"],"font":"Montserrat-Black","base_size":68,"highlight_size":82,"base_color":"&H00FFFFFF&","highlight_color":"&H00EEEEFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.5,"outline_color":"&HFF000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── AURA / ETHEREAL SERIES ──────────────────────────────────────
    "aura_putih": {"name":"Aura Putih Suci","desc":"Cahaya putih aura, spiritual & khidmat","category_match":["quran_hadith","emotional"],"font":"Poppins-SemiBold","base_size":68,"highlight_size":82,"base_color":"&H66FFFFFF&","highlight_color":"&H00FFFFFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":12,"shadow_color":"&H99FFFFFF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "aura_hijau": {"name":"Aura Hijau Langit","desc":"Aura hijau langit, konten surga & rahmat","category_match":["quran_hadith","emotional"],"font":"Poppins-SemiBold","base_size":68,"highlight_size":82,"base_color":"&H6688FF88&","highlight_color":"&H0033CC00&","bold":0,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":11,"shadow_color":"&H7700AA00&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "aura_emas": {"name":"Aura Emas Surgawi","desc":"Aura emas bercahaya, konten akhirat & surga","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Bold","base_size":70,"highlight_size":86,"base_color":"&H66CCCCAA&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":0,"outline_color":"&HFF000000&","shadow_size":11,"shadow_color":"&H7700AAFF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── KARAOKE ADVANCED ────────────────────────────────────────────
    "karaoke_ungu": {"name":"Karaoke Ungu","desc":"Abu jadi ungu aktif, misterius & unik","category_match":["emotional","beginner"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H88AAAAAA&","highlight_color":"&H00FF44FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H66FF00FF&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "karaoke_cyan": {"name":"Karaoke Cyan Fresh","desc":"Abu jadi cyan fresh, modern & energik","category_match":["beginner","viral_quote"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H88AAAAAA&","highlight_color":"&H00FFFF00&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":3,"shadow_color":"&H44FFFF00&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "karaoke_oranye": {"name":"Karaoke Oranye","desc":"Abu jadi oranye, hangat & semangat","category_match":["beginner","emotional"],"font":"Montserrat-Bold","base_size":68,"highlight_size":82,"base_color":"&H88AAAAAA&","highlight_color":"&H000055FF&","bold":1,"italic":0,"border_style":1,"outline_thickness":2.0,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H44FF4400&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── MINIMALIS ADVANCED ──────────────────────────────────────────
    "minimalis_biru": {"name":"Minimalis Biru Tenang","desc":"Biru tenang, cocok topik ilmu & sains","category_match":["knowledge","beginner"],"font":"Poppins-SemiBold","base_size":62,"highlight_size":76,"base_color":"&H00CCDDFF&","highlight_color":"&H00AABBFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":1.5,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H33000044&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "minimalis_coklat": {"name":"Minimalis Coklat Earthy","desc":"Coklat earth tone, hangat & membumi","category_match":["knowledge","emotional"],"font":"Poppins-Regular","base_size":60,"highlight_size":72,"base_color":"&H00BBDDFF&","highlight_color":"&H0099CCFF&","bold":0,"italic":0,"border_style":1,"outline_thickness":1.5,"outline_color":"&HFF000000&","shadow_size":2,"shadow_color":"&H33000033&","mode":"highlight","words_per_block":4,"vertical_position":120,"alignment":2,"remove_punctuation":False},
    "minimalis_hitam": {"name":"Minimalis Hitam Bold","desc":"Hitam bold simpel, keterbacaan max","category_match":["knowledge","viral_quote"],"font":"Montserrat-Bold","base_size":66,"highlight_size":80,"base_color":"&H00444444&","highlight_color":"&H00111111&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCCEEEEEE&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

    # ─── KOMBINASI UNIK ──────────────────────────────────────────────
    "neon_box_ungu": {"name":"Neon Box Ungu","desc":"Teks neon di box ungu gelap, sangat viral","category_match":["viral_quote","beginner"],"font":"Montserrat-Black","base_size":70,"highlight_size":86,"base_color":"&H00FFAAFF&","highlight_color":"&H00FFFFFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HCC220044&","shadow_size":5,"shadow_color":"&H66FF00FF&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "emas_box_hitam": {"name":"Emas di Box Hitam","desc":"Teks emas di box hitam, paling premium","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Black","base_size":70,"highlight_size":86,"base_color":"&H00CCBB88&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":3,"outline_thickness":0,"outline_color":"&HDD000000&","shadow_size":0,"shadow_color":"&H00000000&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "putih_outline_emas": {"name":"Putih + Outline Emas","desc":"Teks putih outline emas, elegan banget","category_match":["quran_hadith","emotional"],"font":"Montserrat-Black","base_size":70,"highlight_size":86,"base_color":"&H00FFFFFF&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":4.0,"outline_color":"&HFF1E3A6E&","shadow_size":3,"shadow_color":"&H441E3A6E&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},
    "wbw_tengah_emas": {"name":"WxW Tengah Emas","desc":"Satu kata emas di tengah layar, epik","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Black","base_size":90,"highlight_size":108,"base_color":"&H00AAAAAA&","highlight_color":"&H0000CCFF&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.5,"outline_color":"&HFF000000&","shadow_size":6,"shadow_color":"&H440066AA&","mode":"word_by_word","words_per_block":1,"vertical_position":900,"alignment":2,"remove_punctuation":True},
    "bold_hijau_xl": {"name":"Bold Hijau XL","desc":"Hijau besar extra bold, dakwah paling impak","category_match":["quran_hadith","viral_quote"],"font":"Montserrat-Black","base_size":80,"highlight_size":96,"base_color":"&H00FFFFFF&","highlight_color":"&H0022DD22&","bold":1,"italic":0,"border_style":1,"outline_thickness":3.5,"outline_color":"&HFF003300&","shadow_size":3,"shadow_color":"&H44006600&","mode":"highlight","words_per_block":3,"vertical_position":120,"alignment":2,"remove_punctuation":True},

}


# ─── Helper Functions ─────────────────────────────────────────────────────────

def get_style(style_key: str) -> dict:
    """Ambil satu style berdasarkan key-nya."""
    style = STYLES.get(style_key)
    if not style:
        available = ", ".join(STYLES.keys())
        raise ValueError(f"Style '{style_key}' tidak ada.\nPilihan: {available}")
    return dict(style)


def list_styles() -> list:
    """Return list semua style dengan info singkat."""
    return [
        {
            "key": key,
            "name": s["name"],
            "desc": s["desc"],
            "category_match": s.get("category_match", []),
            "mode": s.get("mode", "highlight"),
        }
        for key, s in STYLES.items()
    ]


def recommend_styles(category: str, top_n: int = 3) -> list:
    """
    Rekomendasikan style terbaik berdasarkan kategori klip.
    
    Args:
        category: "knowledge" | "viral_quote" | "emotional" | "quran_hadith" | "beginner"
        top_n: jumlah rekomendasi
    
    Returns:
        list of (key, style_dict)
    """
    matched = [
        (key, s) for key, s in STYLES.items()
        if category in s.get("category_match", [])
    ]
    # Fallback kalau tidak ada match
    if not matched:
        matched = list(STYLES.items())

    return [(k, dict(s)) for k, s in matched[:top_n]]


def get_style_preview_text(style_key: str) -> str:
    """
    Return deskripsi style yang cocok untuk ditampilkan di Web UI.
    """
    s = STYLES.get(style_key, {})
    mode_label = {
        "highlight": "Highlight kata aktif",
        "word_by_word": "Kata per kata",
        "no_highlight": "Teks blok, tanpa highlight",
    }.get(s.get("mode", ""), "")

    return (
        f"{s.get('name', style_key)}\n"
        f"{s.get('desc', '')}\n"
        f"Mode: {mode_label} | "
        f"Font: {s.get('font','?')} | "
        f"Ukuran: {s.get('base_size','?')}→{s.get('highlight_size','?')}px"
    )


# ─── Quick Reference ──────────────────────────────────────────────────────────

STYLE_BY_CATEGORY = {
    "knowledge":    ["hormozi_hijau", "cinema_putih", "no_highlight_clean", "box_hijau_islam", "underline_bersih"],
    "viral_quote":  ["hormozi_kuning", "tebal_besar", "glow_emas", "box_hitam", "word_by_word_kuning", "premium_dark", "fire_orange"],
    "emotional":    ["soft_dakwah", "news_merah", "shadow_dramatis", "italic_elegan", "word_by_word_hijau", "fire_orange"],
    "quran_hadith": ["hormozi_hijau", "arabic_style", "glow_emas", "karaoke_emas", "shadow_dramatis", "premium_dark"],
    "beginner":     ["soft_dakwah", "minimalis_putih", "cyan_modern", "no_highlight_clean", "underline_bersih", "dualcolor_ungu"],
}
