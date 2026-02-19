"""
MahiraClipper — Prompt Engine
Semua prompt Gemini untuk analisis konten dakwah/ceramah.
"""

# ─── Prompt Utama Analisis Dakwah ─────────────────────────────────────────────

DAKWAH_ANALYSIS_PROMPT = """
Kamu adalah kurator konten dakwah Islam dan editor video short-form yang ahli.
Tugasmu: analisis transkrip ceramah/kajian Islam dan temukan segmen terbaik untuk dijadikan klip viral di TikTok, Instagram Reels, dan YouTube Shorts.

## KRITERIA PEMILIHAN (prioritas berurutan):

### 1. ILMU PADAT (Knowledge)
- Penjelasan hukum Islam yang jelas dan ringkas
- Tafsir ayat Al-Quran atau penjelasan hadits yang mudah dipahami
- Konsep Islam yang dijelaskan untuk pemula / non-Muslim
- Pelajaran yang bisa langsung diamalkan

### 2. KUTIPAN VIRAL (Viral Quote)
- Kalimat powerful yang bikin penonton berhenti scroll
- Analogi modern yang relate dengan kehidupan sehari-hari
- Nasihat yang singkat, padat, dan menohok
- Kalimat yang layak dijadikan caption atau quote card

### 3. MOMEN EMOSIONAL (Emotional)
- Nada suara pembicara berubah — lebih lembut, tegas, atau bergetar
- Kisah tentang kematian, akhirat, taubat, atau ujian hidup
- Peringatan keras yang membuat penonton merenung
- Momen yang berpotensi membuat penonton menangis atau tersentuh

### 4. AYAT / HADITS + PENJELASAN (Quran/Hadith)
- Pembicara membaca ayat/hadits LALU menjelaskannya
- Wajib ada penjelasannya — jangan ambil bacaan saja tanpa tafsir
- Lebih diutamakan jika penjelasannya dalam bahasa yang mudah dipahami

### 5. RAMAH PEMULA (Beginner-Friendly)
- Menjawab pertanyaan umum tentang Islam
- Penjelasan yang tidak butuh latar belakang ilmu Islam
- Cocok untuk penonton yang baru kenal Islam atau ingin belajar

## YANG HARUS DIHINDARI:
- Segmen yang hanya berisi doa/dzikir tanpa penjelasan
- Penggalan cerita yang tidak punya konteks sendiri
- Bacaan Arab panjang tanpa terjemah atau penjelasan
- Pembukaan/penutupan ceramah (salam, perkenalan, terima kasih)
- Pengumuman atau info administrasi acara
- Segmen yang mengandung kontroversi politik

## PENANGANAN BAHASA:
- Ceramah bisa dalam Bahasa Indonesia, Arab, Inggris, atau campuran
- Jika ada bacaan Arab, tetap valid selama ada penjelasan setelahnya
- Prioritaskan segmen yang pesannya jelas dalam bahasa apapun

## FORMAT OUTPUT:
Balas HANYA dengan JSON valid. Tanpa markdown, tanpa penjelasan, tanpa kode blocks.

{{
  "segments": [
    {{
      "title": "Judul singkat menarik maksimal 8 kata",
      "start_time_ref": "kalimat PERSIS dari transkrip dimana segmen MULAI",
      "end_time_ref": "kalimat PERSIS dari transkrip dimana segmen BERAKHIR",
      "duration": 0,
      "hook": "Kalimat pembuka klip ini — kenapa penonton tidak akan skip?",
      "category": "knowledge|viral_quote|emotional|quran_hadith|beginner",
      "viral_score": 8.5,
      "caption_suggestion": "Saran caption untuk TikTok/IG (bisa pakai emoji)",
      "hashtags": ["#dakwah", "#ceramah", "#islam"],
      "reason": "Satu kalimat: kenapa segmen ini layak dijadikan klip"
    }}
  ],
  "video_summary": "Ringkasan singkat isi ceramah ini dalam 2-3 kalimat",
  "dominant_theme": "Tema utama ceramah (misal: taubat, sholat, kematian, dll)",
  "speaker_style": "deskripsi singkat gaya bicara penceramah"
}}

## ATURAN PENTING:
- Pilih antara {min_clips} sampai {max_clips} segmen terbaik
- Durasi tiap segmen: {min_duration} sampai {max_duration} detik saat dibacakan
- Segmen TIDAK BOLEH overlap satu sama lain
- viral_score adalah float 1.0 sampai 10.0
- Urutkan dari viral_score tertinggi ke terendah
- start_time_ref dan end_time_ref HARUS kata/kalimat yang ada di transkrip

## TRANSKRIP:
{transcript}
"""

# ─── Prompt Generate Caption ──────────────────────────────────────────────────

CAPTION_PROMPT = """
Kamu adalah social media manager konten dakwah Islam yang berpengalaman.
Buatkan caption menarik untuk short video ini berdasarkan judul dan kontennya.

Judul klip: {title}
Kategori: {category}
Hook: {hook}
Tema ceramah: {theme}

Buatkan 3 versi caption:
1. PENDEK (maks 100 karakter) - cocok untuk TikTok
2. SEDANG (100-200 karakter) - cocok untuk Instagram  
3. PANJANG (200-400 karakter) - cocok untuk YouTube Shorts

Balas HANYA dengan JSON:
{{
  "short": "caption pendek + emoji",
  "medium": "caption sedang + emoji + 3-5 hashtag",
  "long": "caption panjang + emoji + 5-10 hashtag",
  "hashtags_suggested": ["#dakwah", "#ceramah", "#islamindonesia"]
}}
"""

# ─── Prompt Validasi Segmen ───────────────────────────────────────────────────

VALIDATION_PROMPT = """
Kamu adalah editor konten dakwah. Review segmen klip ini dan nilai kelayakannya.

Transkrip segmen:
{segment_transcript}

Nilai aspek berikut (skala 1-10) dan balas HANYA dengan JSON:
{{
  "completeness": 8,
  "clarity": 9,
  "islamic_value": 9,
  "viral_potential": 7,
  "is_standalone": true,
  "issues": ["list masalah jika ada, kosong jika tidak ada"],
  "recommendation": "keep|trim_start|trim_end|skip",
  "trim_note": "penjelasan jika perlu di-trim"
}}
"""

# ─── Kategori Label (untuk UI) ────────────────────────────────────────────────

CATEGORY_LABELS = {
    "knowledge":     {"label": "Ilmu Padat",      "emoji": "📚", "color": "#3b82f6"},
    "viral_quote":   {"label": "Kutipan Viral",    "emoji": "💡", "color": "#f59e0b"},
    "emotional":     {"label": "Emosional",        "emoji": "💚", "color": "#10b981"},
    "quran_hadith":  {"label": "Quran / Hadits",   "emoji": "📖", "color": "#8b5cf6"},
    "beginner":      {"label": "Ramah Pemula",     "emoji": "🌱", "color": "#06b6d4"},
}

# ─── Default Hashtags per Kategori ───────────────────────────────────────────

DEFAULT_HASHTAGS = {
    "knowledge":    ["#dakwah", "#ilmuislam", "#ceramah", "#kajianislam", "#muslimIndonesia"],
    "viral_quote":  ["#dakwah", "#nasihatislam", "#quotedakwah", "#islamicquotes", "#ceramah"],
    "emotional":    ["#dakwah", "#ceramahislam", "#tausiyah", "#menangis", "#menyentuh"],
    "quran_hadith": ["#quran", "#hadits", "#dakwah", "#tafsir", "#belajarislam"],
    "beginner":     ["#islamforbeginners", "#belajarislam", "#dakwah", "#islamitu", "#pemula"],
}
