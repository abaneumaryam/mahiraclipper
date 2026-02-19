'use strict'

const S = {
  page:          'home',
  sourceType:    'url',
  filePath:      null,
  clips:         [],
  finalFolder:   null,
  processing:    false,
  styles:        [],
  unsubPipeline: null,
  outputFormat:  { ratio: '9:16', w: 1080, h: 1920 },
  projectName:   '',
}

const PLATFORMS = [
  { re: /youtube\.com|youtu\.be/i,  icon: '▶️', label: 'YouTube'   },
  { re: /instagram\.com/i,          icon: '📸', label: 'Instagram' },
  { re: /facebook\.com|fb\.watch/i, icon: '👥', label: 'Facebook'  },
  { re: /tiktok\.com/i,             icon: '🎵', label: 'TikTok'    },
  { re: /twitter\.com|x\.com/i,     icon: '🐦', label: 'Twitter/X' },
]

const CAT = {
  knowledge:    { color: '#2563eb', bg: '#eff6ff', label: '📚 Ilmu'   },
  viral_quote:  { color: '#b45309', bg: '#fffbeb', label: '💡 Viral'  },
  emotional:    { color: '#2D6B42', bg: '#E3F0E8', label: '💚 Emosi'  },
  quran_hadith: { color: '#6d28d9', bg: '#f5f3ff', label: '📖 Quran'  },
  beginner:     { color: '#0e7490', bg: '#ecfeff', label: '🌱 Pemula' },
}

// ── Boot ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  // Init ads dulu
  await AdManager.init()

  // Splash screen
  await showSplash()

  initTitlebar()
  initNav()
  initHomeForm()
  initFormatGrid()
  await loadStyles()
  await loadConfig()
})

async function showSplash() {
  const splash = document.getElementById('splash-screen')
  if (!splash) return

  // Tampilkan iklan di splash setelah 1 detik
  AdManager.show('splash', 'ad-banner-splash')

  const data    = await window.app.getAds().catch(() => ({ settings: {} }))
  const durSec  = (data.settings?.splash_duration_sec ?? 3) * 1000

  return new Promise(resolve => {
    setTimeout(() => {
      splash.classList.add('fade-out')
      AdManager.hide('ad-banner-splash')
      setTimeout(() => {
        splash.classList.add('hidden')
        resolve()
      }, 500)
    }, durSec)
  })
}

// ── Titlebar ──────────────────────────────────────────────────────────────────
function initTitlebar() {
  document.getElementById('tc-min').onclick = () => window.app.minimize()
  document.getElementById('tc-max').onclick = () => window.app.maximize()
  document.getElementById('tc-cls').onclick = () => window.app.close()
}

// ── Navigation ────────────────────────────────────────────────────────────────
function initNav() {
  document.querySelectorAll('.nav').forEach(btn => {
    btn.onclick = () => goPage(btn.dataset.page)
  })
  document.getElementById('btn-refresh')?.addEventListener('click', loadHistory)
}

function goPage(page) {
  S.page = page
  document.querySelectorAll('.nav').forEach(b =>
    b.classList.toggle('active', b.dataset.page === page))
  document.querySelectorAll('.page').forEach(p =>
    p.classList.toggle('active', p.id === `page-${page}`))
  if (page === 'history') loadHistory()
  if (page === 'styles')  renderStyles('all')
  if (page === 'settings') syncSettingsUI()
  if (page === 'about') initAboutPage()
}

// ── Format Grid ───────────────────────────────────────────────────────────────
function initFormatGrid() {
  document.querySelectorAll('.format-card').forEach(card => {
    card.onclick = () => {
      document.querySelectorAll('.format-card').forEach(c => c.classList.remove('active'))
      card.classList.add('active')
      S.outputFormat = {
        ratio: card.dataset.format,
        w:     parseInt(card.dataset.w),
        h:     parseInt(card.dataset.h),
      }
      // Update badge face tracking (16:9 tidak perlu crop ke vertikal)
      const isLandscape = S.outputFormat.ratio === '16:9'
      const cropChip    = document.getElementById('chip-focus-mode')
      const cropChk     = document.getElementById('chk-crop')
      if (isLandscape) {
        cropChk.checked = false
        if (cropChip) cropChip.style.opacity = '0.4'
        toast('Format 16:9 — crop dinonaktifkan', '')
      } else {
        if (cropChip) cropChip.style.opacity = '1'
      }
    }
  })
}

// ── Home Form ─────────────────────────────────────────────────────────────────
function initHomeForm() {
  // Source type
  document.querySelectorAll('.pill').forEach(pill => {
    pill.onclick = () => {
      document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'))
      pill.classList.add('active')
      S.sourceType = pill.dataset.src
      document.getElementById('wrap-url').classList.toggle('hidden', S.sourceType !== 'url')
      document.getElementById('wrap-file').classList.toggle('hidden', S.sourceType !== 'file')
    }
  })

  // URL detect
  document.getElementById('inp-url').addEventListener('input', e => detectPlatform(e.target.value))

  // Paste
  document.getElementById('btn-paste').onclick = async () => {
    try {
      const text = await navigator.clipboard.readText()
      document.getElementById('inp-url').value = text.trim()
      detectPlatform(text.trim())
    } catch { toast('Tidak bisa akses clipboard', 'err') }
  }

  // Drop zone
  const dz = document.getElementById('drop-zone')
  dz.onclick = async () => {
    const p = await window.app.pickFile()
    if (p) setFile(p)
  }
  dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('over') })
  dz.addEventListener('dragleave', () => dz.classList.remove('over'))
  dz.addEventListener('drop', e => {
    e.preventDefault(); dz.classList.remove('over')
    const f = e.dataTransfer.files[0]
    if (f) {
      const filePath = window.app.getFilePath(f)
      if (filePath) setFile(filePath)
      else toast('Gagal baca path. Coba pakai tombol Pilih File.', 'err')
    }
  })

  document.getElementById('btn-browse').onclick = async (e) => {
    e.stopPropagation()
    const p = await window.app.pickFile()
    if (p) setFile(p)
  }

  document.getElementById('file-clear').onclick = () => {
    S.filePath = null
    document.getElementById('file-chosen').classList.add('hidden')
    document.getElementById('drop-zone').classList.remove('hidden')
  }

  // Steppers
  document.querySelectorAll('.step-btn').forEach(btn => {
    btn.onclick = () => {
      const el  = document.getElementById(btn.dataset.target)
      const cur = parseInt(el.textContent)
      el.textContent = Math.min(
        parseInt(btn.dataset.max),
        Math.max(parseInt(btn.dataset.min), cur + parseInt(btn.dataset.delta))
      )
    }
  })

  // Crop toggle → disable focus mode when off
  document.getElementById('chk-crop').addEventListener('change', e => {
    const chip = document.getElementById('chip-focus-mode')
    if (chip) chip.style.opacity = e.target.checked ? '1' : '0.4'
  })

  // Project name input
  const projNameEl = document.getElementById('inp-project-name')
  const clearNameEl = document.getElementById('btn-clear-name')
  if (projNameEl) {
    projNameEl.addEventListener('input', e => {
      S.projectName = e.target.value.trim()
      if (clearNameEl) clearNameEl.classList.toggle('hidden', !S.projectName)
    })
  }
  if (clearNameEl) {
    clearNameEl.onclick = () => {
      S.projectName = ''
      if (projNameEl) projNameEl.value = ''
      clearNameEl.classList.add('hidden')
    }
  }

  // Auto-fill project name dari URL
  document.getElementById('inp-url').addEventListener('change', e => {
    if (!S.projectName && projNameEl) {
      const url = e.target.value.trim()
      const auto = url.split('?')[0].rstrip?.('/').split('/').pop() || ''
      // Jangan auto-fill jika sudah ada nama
    }
  })

  document.getElementById('btn-process').onclick = startProcess
  document.getElementById('btn-folder').onclick  = () => {
    if (S.finalFolder) window.app.openFolder(S.finalFolder)
  }
}

function detectPlatform(url) {
  const el = document.getElementById('platform-detect')
  if (!url.trim()) { el.innerHTML = ''; return }
  const p = PLATFORMS.find(x => x.re.test(url))
  el.innerHTML = p
    ? `<span class="platform-badge">${p.icon} ${p.label} terdeteksi</span>`
    : `<span style="color:var(--text-3);font-size:0.78rem">Link tidak dikenal — akan dicoba via yt-dlp</span>`
}

function setFile(path) {
  S.filePath = path
  const name = path.split(/[\\/]/).pop()
  document.getElementById('file-name').textContent = name
  document.getElementById('file-path-display').textContent = path
  document.getElementById('drop-zone').classList.add('hidden')
  document.getElementById('file-chosen').classList.remove('hidden')
}

// ── Pipeline ──────────────────────────────────────────────────────────────────
async function startProcess() {
  const url  = document.getElementById('inp-url').value.trim()
  const file = S.filePath

  if (S.sourceType === 'url'  && !url)  { toast('Masukkan URL dulu ya!',    'err'); return }
  if (S.sourceType === 'file' && !file) { toast('Pilih file video dulu ya!', 'err'); return }

  const cfg    = await window.app.getConfig()
  const apiKey = (cfg.groq && cfg.groq.api_key) || ''
  if (!apiKey || apiKey.length < 10) {
    toast('Groq API key belum diisi! Buka Settings dulu.', 'err')
    goPage('settings')
    return
  }

  const durVal  = document.getElementById('sel-duration').value
  const [minDur, maxDur] = durVal.split(',').map(Number)
  const doCrop  = document.getElementById('chk-crop').checked
  const cropMode = document.getElementById('sel-crop-mode').value

  const payload = {
    url:          S.sourceType === 'url'  ? url  : '',
    file:         S.sourceType === 'file' ? file : '',
    project_name: S.projectName || '',
    num_clips:    parseInt(document.getElementById('val-clips').textContent),
    min_dur:      minDur,
    max_dur:      maxDur,
    do_crop:      doCrop,
    crop_mode:    cropMode,
    style_key:    document.getElementById('sel-style').value || null,
    font_size:      parseInt(document.getElementById('val-fontsize')?.textContent || '0'),
    v_position:     document.querySelector('input[name="vpos"]:checked')?.value || 'bottom',
    groq_api_key:   apiKey,
    groq_model:     (cfg.groq && cfg.groq.model) || 'llama-3.3-70b-versatile',
    whisper_model:  (cfg.whisper && cfg.whisper.model_size) || 'small',
    whisper_lang:   (cfg.whisper && cfg.whisper.language) || 'id',
    output_w:     S.outputFormat.w,
    output_h:     S.outputFormat.h,
    output_ratio: S.outputFormat.ratio,
  }

  // Reset UI
  S.processing = true; S.clips = []; S.finalFolder = null
  const btn = document.getElementById('btn-process')
  btn.disabled = true
  btn.innerHTML = '<span class="spin">⟳</span> Memproses...'

  // Tampilkan iklan saat proses berjalan
  AdManager.show('processing', 'ad-banner-fixed')
  document.getElementById('process-panel').classList.remove('hidden')
  document.getElementById('clips-preview').classList.add('hidden')
  document.getElementById('btn-folder').classList.add('hidden')
  document.getElementById('log-panel').innerHTML = ''
  document.getElementById('prog-bar').style.width = '0%'
  document.getElementById('clips-title').textContent = 'Momen Terdeteksi'
  resetSteps()

  if (S.unsubPipeline) S.unsubPipeline()
  S.unsubPipeline = window.app.onPipelineEvent(handlePipelineEvent)
  window.app.runPipeline(payload)
}

function handlePipelineEvent(data) {
  switch (data.event) {
    case 'log':
      appendLog(data.msg, data.level)
      break
    case 'progress':
      setProgress(data.step, data.pct)
      break
    case 'project_created':
      appendLog('Project: ' + data.name)
      break
    case 'clips':
      S.clips = data.clips || []
      renderClipsList(S.clips)
      document.getElementById('clips-preview').classList.remove('hidden')
      document.getElementById('clips-title').textContent =
        `🧠 ${S.clips.length} Momen Terdeteksi Gemini AI`
      break
    case 'done':
      S.finalFolder = data.final_folder
      S.clips       = data.clips || []
      renderClipsList(S.clips)
      document.getElementById('clips-preview').classList.remove('hidden')
      document.getElementById('btn-folder').classList.remove('hidden')
      document.getElementById('clips-title').textContent = `🎉 ${S.clips.length} Klip Siap!`
      finishProcess(true)
      toast('Alhamdulillah, semua klip siap! 🎉', 'ok')
      // Ganti iklan ke konteks 'done'
      AdManager.show('done', 'ad-banner-fixed')
      break
    case 'error':
      appendLog('❌ ' + data.msg, 'err')
      finishProcess(false)
      toast(data.msg.slice(0, 80), 'err')
      break
  }
}

function finishProcess(ok) {
  S.processing = false
  const btn = document.getElementById('btn-process')
  btn.disabled = false
  btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg> Mulai Proses`
  if (S.unsubPipeline) { S.unsubPipeline(); S.unsubPipeline = null }
  // Kalau error, sembunyikan iklan
  if (!ok) AdManager.hide('ad-banner-fixed')
}

// ── Steps ─────────────────────────────────────────────────────────────────────
const STEP_ORDER = ['download','gemini','cut','crop','subtitle']

function resetSteps() {
  STEP_ORDER.forEach(step => {
    const el = document.querySelector(`.step-item[data-step="${step}"]`)
    if (!el) return
    el.classList.remove('running','done','error')
    el.querySelector('.step-state').textContent = 'Menunggu'
  })
}

function setProgress(step, pct) {
  document.getElementById('prog-bar').style.width = pct + '%'
  const idx = STEP_ORDER.indexOf(step)
  STEP_ORDER.forEach((s, i) => {
    const el = document.querySelector(`.step-item[data-step="${s}"]`)
    if (!el) return
    const stEl = el.querySelector('.step-state')
    el.classList.remove('running','done','error')
    if      (i < idx)  { el.classList.add('done');    stEl.textContent = 'Selesai ✓' }
    else if (s === step){ el.classList.add('running'); stEl.textContent = pct + '%'   }
  })
}

// ── Log ───────────────────────────────────────────────────────────────────────
function appendLog(msg, level = 'info') {
  const panel = document.getElementById('log-panel')
  const line  = document.createElement('span')
  line.className   = 'log-line' + (level === 'err' || level === 'error' ? ' err' : level === 'warn' ? ' warn' : level === 'ok' ? ' ok' : '')
  line.textContent = msg
  panel.appendChild(line)
  panel.appendChild(document.createTextNode('\n'))
  panel.scrollTop = panel.scrollHeight
}

// ── Clips ─────────────────────────────────────────────────────────────────────
function renderClipsList(clips) {
  const list = document.getElementById('clips-list')
  if (!clips.length) { list.innerHTML = ''; return }

  list.innerHTML = clips.map((c, i) => {
    const cat   = CAT[c.category] || CAT.knowledge
    const isDone = c.is_subtitled || c.final_path
    const score  = parseFloat(c.viral_score || 0).toFixed(1)
    const dur    = Math.round(c.duration || 0)
    const hook   = c.hook ? `<div style="font-size:0.72rem;color:var(--text-3);margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">"${esc(c.hook)}"</div>` : ''

    const badges = [
      `<span class="clip-badge" style="color:${cat.color};border-color:${cat.color}44;background:${cat.bg}">${cat.label}</span>`,
      `<span class="clip-badge" style="color:var(--text-3);border-color:var(--border);background:transparent">⏱ ${dur}s</span>`,
    ].join('')

    return `
    <div class="clip-row" style="animation-delay:${i*0.05}s">
      <div class="clip-num">${String(i+1).padStart(2,'0')}</div>
      <div class="clip-body">
        <div class="clip-title-text">${esc(c.title || '')}</div>
        ${hook}
        <div class="clip-meta" style="margin-top:5px">${badges}</div>
      </div>
      <div class="clip-right">
        <div class="clip-score">★ ${score}</div>
        <div class="clip-dur">${dur}s</div>
        <div class="clip-status-text ${isDone ? 'done' : ''}">${isDone ? '✓ Siap' : '⏳'}</div>
      </div>
    </div>`
  }).join('')
}

// ── History ───────────────────────────────────────────────────────────────────
async function loadHistory() {
  const el = document.getElementById('history-list')
  el.innerHTML = '<div class="empty-hint">Memuat...</div>'
  const projects = await window.app.getProjects()
  if (!projects.length) {
    el.innerHTML = '<div class="empty-hint">Belum ada project 🌱<br><span style="font-size:0.78rem">Proses video pertamamu di Beranda</span></div>'
    return
  }
  el.innerHTML = projects.map((p, i) => {
    const status  = p.status || 'created'
    const date    = (p.updated_at || '').slice(0,16).replace('T',' ')
    const clips   = Array.isArray(p.clips) ? p.clips.length : (p.clips || 0)
    const isDone  = status === 'done'
    const hasFinal = p.folder

    return `
    <div class="history-card" style="animation-delay:${i*0.04}s" onclick="openProjectModal('${p.id}')">
      <div class="h-dot ${status}"></div>
      <div class="h-info">
        <div class="h-name">${esc(p.name || p.id)}</div>
        <div class="h-meta">
          <span>🕐 ${date}</span>
          ${p.dominant_theme ? `<span>🎯 ${esc(p.dominant_theme)}</span>` : ''}
          ${p.source_platform ? `<span>${platformIcon(p.source_platform)} ${p.source_platform}</span>` : ''}
        </div>
      </div>
      <div class="h-right">
        <span class="h-clips-badge">${clips} klip</span>
        <div class="h-actions" onclick="event.stopPropagation()">
          ${isDone ? `<button class="btn-h-action" onclick="openProjectFolder('${p.id}','final')">📂 Klip</button>` : ''}
          <button class="btn-h-action" onclick="openProjectFolder('${p.id}','root')">📁 Folder</button>
          <button class="btn-h-action red btn-del" onclick="deleteProject('${p.id}')">🗑</button>
        </div>
      </div>
    </div>`
  }).join('')

  // Tombol buka folder semua projects
  const btnProj = document.getElementById('btn-open-projects-folder')
  if (btnProj) btnProj.onclick = () => window.app.openProjectsFolder()
}

async function openProjectFolder(id, type) {
  const projects = await window.app.getProjects()
  const p = projects.find(x => x.id === id)
  if (!p || !p.folder) { toast('Folder tidak ditemukan', 'err'); return }
  const folder = type === 'final'
    ? p.folder + '/final'
    : p.folder
  window.app.openFolder(folder)
}

async function openProjectModal(id) {
  const projects = await window.app.getProjects()
  const p = projects.find(x => x.id === id)
  if (!p) return

  const clips   = Array.isArray(p.clips) ? p.clips : []
  const date    = (p.created_at || '').slice(0,16).replace('T',' ')
  const updated = (p.updated_at || '').slice(0,16).replace('T',' ')
  const status  = p.status || 'created'
  const statusLabel = { done:'✅ Selesai', running:'⏳ Berjalan', failed:'❌ Gagal', error:'❌ Error', created:'🆕 Dibuat' }

  const clipsHtml = clips.length ? clips.map((c, i) => {
    const cat   = CAT[c.category] || CAT.knowledge
    const score = parseFloat(c.viral_score || 0).toFixed(1)
    const dur   = Math.round(c.duration || 0)
    const hasFinal = c.final_path || c.is_subtitled
    return `
    <div class="modal-clip-row">
      <div class="modal-clip-num">${String(i+1).padStart(2,'0')}</div>
      <div class="modal-clip-info">
        <div class="modal-clip-title">${esc(c.title || 'Klip ' + (i+1))}</div>
        <div class="modal-clip-meta">
          <span style="color:${cat.color}">${cat.label}</span>
          &nbsp;·&nbsp; ⏱ ${dur}s &nbsp;·&nbsp; ★ ${score}
        </div>
      </div>
      <div class="modal-clip-actions">
        ${hasFinal ? `<button class="btn-mini" onclick="openClipFile('${esc(c.final_path || '')}')">▶ Buka</button>` : ''}
        ${c.raw_cut_path ? `<button class="btn-mini" onclick="openClipFile('${esc(c.raw_cut_path || '')}')">📄 Raw</button>` : ''}
      </div>
    </div>`
  }).join('') : '<div style="color:var(--text-3);font-size:0.85rem;padding:8px 0">Belum ada klip</div>'

  document.getElementById('modal-title').textContent = p.name || p.id
  document.getElementById('modal-body').innerHTML = `
    <div class="modal-info-grid">
      <div class="modal-info-item">
        <div class="modal-info-label">Status</div>
        <div class="modal-info-value">${statusLabel[status] || status}</div>
      </div>
      <div class="modal-info-item">
        <div class="modal-info-label">Klip</div>
        <div class="modal-info-value">${clips.length} klip</div>
      </div>
      <div class="modal-info-item">
        <div class="modal-info-label">Dibuat</div>
        <div class="modal-info-value">${date}</div>
      </div>
      <div class="modal-info-item">
        <div class="modal-info-label">Platform</div>
        <div class="modal-info-value">${platformIcon(p.source_platform)} ${p.source_platform || 'lokal'}</div>
      </div>
      ${p.dominant_theme ? `
      <div class="modal-info-item" style="grid-column:1/-1">
        <div class="modal-info-label">Tema</div>
        <div class="modal-info-value">🎯 ${esc(p.dominant_theme)}</div>
      </div>` : ''}
      ${p.video_summary ? `
      <div class="modal-info-item" style="grid-column:1/-1">
        <div class="modal-info-label">Ringkasan</div>
        <div class="modal-info-value" style="font-weight:500;font-size:0.82rem;line-height:1.5">${esc(p.video_summary)}</div>
      </div>` : ''}
    </div>

    <div class="modal-section-title">🎬 Daftar Klip</div>
    ${clipsHtml}

    <div class="modal-actions-row">
      ${p.folder ? `<button class="btn-modal-action primary" onclick="window.app.openFolder('${p.folder}/final');closeModal()">📂 Buka Folder Klip Final</button>` : ''}
      ${p.folder ? `<button class="btn-modal-action" onclick="window.app.openFolder('${p.folder}');closeModal()">📁 Buka Folder Project</button>` : ''}
      <button class="btn-modal-action danger" onclick="deleteProject('${p.id}');closeModal()">🗑 Hapus Project</button>
    </div>
  `

  document.getElementById('modal-backdrop').classList.remove('hidden')
}

function closeModal() {
  document.getElementById('modal-backdrop').classList.add('hidden')
}

function openClipFile(path) {
  if (path) window.app.openFolder(require ? path.replace(/[^/\\]*$/, '') : path)
}

function platformIcon(p) {
  const m = { youtube:'▶️', instagram:'📸', facebook:'👥', tiktok:'🎵', local:'📁' }
  return m[p] || '🌐'
}

async function deleteProject(id) {
  if (!confirm('Hapus project ini? File video juga akan terhapus.')) return
  await window.app.deleteProject(id)
  toast('Project dihapus')
  loadHistory()
}

// ── Styles ────────────────────────────────────────────────────────────────────
async function loadStyles() {
  S.styles = getBuiltinStyles()
  const sel = document.getElementById('sel-style')
  sel.innerHTML = '<option value="">Auto ✨</option>' +
    S.styles.map(s => `<option value="${s.key}">${s.name}</option>`).join('')
}

function renderStyles(cat = 'all') {
  document.querySelectorAll('.cat-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.cat === cat))

  const filtered = cat === 'all' ? S.styles : S.styles.filter(s => s.cats.includes(cat))
  const grid = document.getElementById('styles-grid')
  if (!filtered.length) { grid.innerHTML = '<div class="empty-hint">Tidak ada style</div>'; return }

  grid.innerHTML = filtered.map((s, i) => {
    const cats = s.cats.map(c => {
      const cc = CAT[c] || { color: '#22c55e', bg: '#edf5f0', label: c }
      return `<span class="clip-badge" style="color:${cc.color};border-color:${cc.color}44;background:${cc.bg};font-size:0.6rem">${cc.label}</span>`
    }).join('')
    return `
    <div class="style-card" style="animation-delay:${i*0.03}s">
      <div class="style-preview">
        <div class="preview-sub">${buildPreview(s)}</div>
      </div>
      <div class="style-body">
        <div class="style-name-text">${i+1}. ${esc(s.name)}</div>
        <div class="style-desc-text">${esc(s.desc)}</div>
        <div class="style-cats-wrap">${cats}</div>
        <span class="style-key-copy" onclick="copyKey(this,'${s.key}')">${s.key}</span>
      </div>
    </div>`
  }).join('')

  document.querySelectorAll('.cat-btn').forEach(b => {
    b.onclick = () => renderStyles(b.dataset.cat)
  })
}

function buildPreview(s) {
  function assToHex(v = '') {
    const m = v.match(/&H[0-9A-Fa-f]{2}([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})&/)
    return m ? `#${m[3]}${m[2]}${m[1]}` : '#ffffff'
  }
  const hl  = assToHex(s.hlColor)
  const base = assToHex(s.baseColor)
  const outl = s.outline > 0 ? `-webkit-text-stroke:${Math.min(s.outline*0.35,1.2)}px #000` : ''
  const shad = s.shadow  > 0 ? `text-shadow:2px 2px 6px rgba(0,0,0,0.8)` : ''
  const boxSty = s.borderStyle === 3 ? 'background:rgba(0,0,0,0.65);padding:3px 10px;border-radius:5px' : ''
  const words   = ['Allah', 'Maha', 'Pengampun']
  const content = s.mode === 'word_by_word'
    ? `<span style="color:${hl};font-size:1rem;font-weight:900;${outl};${shad}">Sesungguhnya</span>`
    : words.map((w, i) => i === 1
        ? `<span style="color:${hl};font-weight:900">${w}</span>`
        : `<span style="color:${base};opacity:0.8">${w}</span>`
      ).join(' ')
  return `<span style="font-size:0.78rem;font-weight:700;${boxSty};${outl};${shad}">${content}</span>`
}

function copyKey(el, key) {
  navigator.clipboard.writeText(key).catch(() => {})
  el.textContent = '✓ Disalin!'
  el.classList.add('copied')
  setTimeout(() => { el.textContent = key; el.classList.remove('copied') }, 1500)
}

// ── Settings ──────────────────────────────────────────────────────────────────
async function loadConfig() {
  try { syncSettingsUI(await window.app.getConfig()) } catch {}
}

function syncSettingsUI(cfg) {
  if (!cfg) { window.app.getConfig().then(syncSettingsUI); return }
  const g = cfg.groq || {}, w = cfg.whisper || {}, c = cfg.clip || {}
  const $ = id => document.getElementById(id)
  if ($('s-groq-key')    && g.api_key)      $('s-groq-key').value     = g.api_key
  if ($('s-groq-model')  && g.model)        $('s-groq-model').value   = g.model
  if ($('s-whisper-model') && w.model_size) $('s-whisper-model').value = w.model_size
  if ($('s-whisper-auto') && w.language)    $('s-whisper-auto').checked = (w.language === 'auto')
  if ($('s-clips')  && c.num_clips)         $('s-clips').value  = c.num_clips
  if ($('s-min')    && c.min_duration)      $('s-min').value    = c.min_duration
  if ($('s-max')    && c.max_duration)      $('s-max').value    = c.max_duration
  if ($('s-whisper-model')) updateWhisperInfo($('s-whisper-model').value)
}

document.getElementById('s-eye').onclick = () => {
  const inp = document.getElementById('s-groq-key')
  inp.type  = inp.type === 'password' ? 'text' : 'password'
}
document.getElementById('s-getkey').onclick = e => {
  e.preventDefault()
  window.app.openUrl('https://console.groq.com')
}
document.getElementById('btn-save').onclick = async () => {
  const groqKey = document.getElementById('s-groq-key').value.trim()
  if (!groqKey) { toast('Groq API key tidak boleh kosong!', 'err'); return }
  const whisperAutoLang = document.getElementById('s-whisper-auto')?.checked
  await window.app.saveConfig({
    groq: {
      api_key: groqKey,
      model:   document.getElementById('s-groq-model').value,
    },
    whisper: {
      model_size: document.getElementById('s-whisper-model').value,
      language:   whisperAutoLang ? 'auto' : 'id',
    },
    clip: {
      num_clips:    parseInt(document.getElementById('s-clips').value),
      min_duration: parseInt(document.getElementById('s-min').value),
      max_duration: parseInt(document.getElementById('s-max').value),
    },
  })
  document.getElementById('save-msg').textContent = '✓ Tersimpan!'
  setTimeout(() => { document.getElementById('save-msg').textContent = '' }, 3000)
  toast('Pengaturan disimpan ✓', 'ok')
}

// ── Toast ─────────────────────────────────────────────────────────────────────
function toast(msg, type = '') {
  const el = document.getElementById('toast')
  el.textContent = msg; el.className = `toast show ${type}`
  clearTimeout(el._t); el._t = setTimeout(() => { el.className = 'toast' }, 3200)
}

function esc(s) {
  return String(s || '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')
}

function getBuiltinStyles() {
  return [
    { key:'hormozi_kuning',   name:'Hormozi Kuning',    desc:'Bold kuning, viral & tegas',             cats:['viral_quote','knowledge'],    mode:'highlight',    hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:0, borderStyle:1 },
    { key:'hormozi_hijau',    name:'Hormozi Hijau',     desc:'Bold hijau Islam, ayat & hadits',         cats:['quran_hadith','knowledge'],   mode:'highlight',    hlColor:'&H0033CC00&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:0, borderStyle:1 },
    { key:'soft_dakwah',      name:'Soft Dakwah',       desc:'Hijau mint, emosional & menyentuh',       cats:['emotional','beginner'],       mode:'highlight',    hlColor:'&H0090EE90&', baseColor:'&H00F0F0F0&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'cinema_putih',     name:'Cinema Putih',      desc:'Outline tebal, dokumenter profesional',   cats:['knowledge','quran_hadith'],   mode:'highlight',    hlColor:'&H00E0E0E0&', baseColor:'&H00FFFFFF&', outline:3.5, shadow:3, borderStyle:1 },
    { key:'news_merah',       name:'News Merah',        desc:'Merah tegas, peringatan keras',           cats:['emotional'],                  mode:'highlight',    hlColor:'&H000000FF&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:0, borderStyle:1 },
    { key:'box_hitam',        name:'Box Hitam',         desc:'Background box gelap, kuning terbaca',    cats:['viral_quote','knowledge'],    mode:'highlight',    hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    { key:'box_hijau_islam',  name:'Box Hijau Islam',   desc:'Box hijau tua, kajian resmi islami',      cats:['quran_hadith','knowledge'],   mode:'highlight',    hlColor:'&H0090EE90&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    { key:'glow_emas',        name:'Glow Emas',         desc:'Efek glow keemasan, quote penting',       cats:['viral_quote','quran_hadith'], mode:'highlight',    hlColor:'&H0000D4FF&', baseColor:'&H00D4D4D4&', outline:3.0, shadow:4, borderStyle:1 },
    { key:'minimalis_putih',  name:'Minimalis Putih',   desc:'Clean minimalis, fokus penceramah',       cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00CCCCCC&', outline:1.5, shadow:1, borderStyle:1 },
    { key:'cyan_modern',      name:'Cyan Modern',       desc:'Segar & modern, audiens muda',            cats:['beginner','viral_quote'],     mode:'highlight',    hlColor:'&H00FFFF00&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:2, borderStyle:1 },
    { key:'wbw_kuning',       name:'Word×Word Kuning',  desc:'Satu kata satu-satu, dramatis',           cats:['viral_quote','emotional'],    mode:'word_by_word', hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:3.0, shadow:0, borderStyle:1 },
    { key:'wbw_hijau',        name:'Word×Word Hijau',   desc:'Kata per kata hijau, fokus & intens',     cats:['quran_hadith','emotional'],   mode:'word_by_word', hlColor:'&H0033CC00&', baseColor:'&H00FFFFFF&', outline:3.0, shadow:0, borderStyle:1 },
    { key:'karaoke_emas',     name:'Karaoke Emas',      desc:'Abu jadi emas saat aktif, ala lirik',     cats:['viral_quote','quran_hadith'], mode:'highlight',    hlColor:'&H0000D4FF&', baseColor:'&H88AAAAAA&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'tebal_besar',      name:'Tebal Besar',       desc:'Font jumbo super bold, max impact',       cats:['viral_quote'],                mode:'word_by_word', hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:4.0, shadow:0, borderStyle:1 },
    { key:'italic_elegan',    name:'Italic Elegan',     desc:'Italic oranye, elegan & bijaksana',       cats:['emotional','beginner'],       mode:'highlight',    hlColor:'&H000088FF&', baseColor:'&H00E8E8E8&', outline:2.0, shadow:3, borderStyle:1 },
    { key:'shadow_dramatis',  name:'Shadow Dramatis',   desc:'Shadow tebal, sinematik mendalam',        cats:['emotional','quran_hadith'],   mode:'highlight',    hlColor:'&H0090EE90&', baseColor:'&H00FFFFFF&', outline:0,   shadow:6, borderStyle:1 },
    { key:'underline_bersih', name:'Underline Bersih',  desc:'Underline aktif, bersih tanpa warna',     cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00DDDDDD&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'dualcolor_ungu',   name:'Dualcolor Ungu',    desc:'Highlight ungu/magenta, modern beda',     cats:['beginner','viral_quote'],     mode:'highlight',    hlColor:'&H00FF44CC&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:2, borderStyle:1 },
    { key:'no_highlight',     name:'No Highlight',      desc:'Tanpa highlight, putih bersih',           cats:['knowledge','beginner'],       mode:'no_highlight', hlColor:'&H00FFFFFF&', baseColor:'&H00FFFFFF&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'arabic_style',     name:'Arabic Style',      desc:'Teks Arab + terjemah Indonesia',          cats:['quran_hadith'],               mode:'highlight',    hlColor:'&H0033CC00&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:3, borderStyle:1 },
    { key:'fire_orange',      name:'Fire Orange',       desc:'Oranye menyala, energi tinggi',           cats:['emotional','viral_quote'],    mode:'highlight',    hlColor:'&H000066FF&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:3, borderStyle:1 },
    { key:'premium_dark',     name:'Premium Dark',      desc:'Box gelap tengah, ala quote Instagram',   cats:['viral_quote','quran_hadith'], mode:'highlight',    hlColor:'&H0000D4FF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },

    // ── BATCH 2&3: 50 Style Baru ──────────────────────────────────
    // NEON
    { key:'neon_pink',           name:'Neon Pink',            desc:'Merah jambu neon, anak muda',              cats:['viral_quote','beginner'],     mode:'highlight',    hlColor:'&H00FF44FF&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:3, borderStyle:1 },
    { key:'neon_biru',           name:'Neon Biru Elektrik',   desc:'Biru elektrik futuristik',                 cats:['viral_quote','beginner'],     mode:'highlight',    hlColor:'&H00FF8800&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:3, borderStyle:1 },
    { key:'neon_hijau_gelap',    name:'Neon Hijau Night',     desc:'Hijau neon dramatic night mode',           cats:['viral_quote','emotional'],    mode:'highlight',    hlColor:'&H0000FF88&', baseColor:'&H00AAAAAA&', outline:2.0, shadow:5, borderStyle:1 },
    { key:'neon_oranye',         name:'Neon Oranye Api',      desc:'Oranye neon menyala, energi ekstrem',      cats:['viral_quote','emotional'],    mode:'highlight',    hlColor:'&H000055FF&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:4, borderStyle:1 },
    { key:'neon_cyan_glow',      name:'Neon Cyan Glow',       desc:'Cyan glow terang, tampilan keren',         cats:['viral_quote','beginner'],     mode:'highlight',    hlColor:'&H00FFFF00&', baseColor:'&H00888888&', outline:0,   shadow:8, borderStyle:1 },
    // BOX
    { key:'box_merah',           name:'Box Merah Peringatan', desc:'Box merah tua, peringatan penting',        cats:['emotional','viral_quote'],    mode:'highlight',    hlColor:'&H0044AAFF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    { key:'box_emas',            name:'Box Emas Mewah',       desc:'Box emas mewah, ayat & hadits',            cats:['quran_hadith','viral_quote'], mode:'highlight',    hlColor:'&H0000D4FF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    { key:'box_ungu',            name:'Box Ungu Elegan',      desc:'Box ungu gelap, elegan',                   cats:['emotional','beginner'],       mode:'highlight',    hlColor:'&H00FF88FF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    { key:'box_putih',           name:'Box Putih Bersih',     desc:'Box putih teks gelap, elegant',            cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H002D6B42&', baseColor:'&H00333333&', outline:0,   shadow:0, borderStyle:3 },
    { key:'box_transparan',      name:'Box Semi-Transparan',  desc:'Box hitam transparan, clean & modern',     cats:['knowledge','viral_quote'],    mode:'highlight',    hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    { key:'box_biru_tua',        name:'Box Biru Navy',        desc:'Box navy profesional, serius',             cats:['knowledge','quran_hadith'],   mode:'highlight',    hlColor:'&H00FFCC88&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    // WORD-BY-WORD
    { key:'wbw_merah',           name:'Word×Word Merah Api',  desc:'Kata per kata merah, tegas & keras',       cats:['emotional','viral_quote'],    mode:'word_by_word', hlColor:'&H000000FF&', baseColor:'&H00FFFFFF&', outline:3.0, shadow:2, borderStyle:1 },
    { key:'wbw_emas',            name:'Word×Word Emas',       desc:'Kata per kata emas berkilau',              cats:['quran_hadith','viral_quote'], mode:'word_by_word', hlColor:'&H0000D4FF&', baseColor:'&H00CCCCCC&', outline:3.0, shadow:4, borderStyle:1 },
    { key:'wbw_ungu',            name:'Word×Word Ungu',       desc:'Kata per kata ungu, misterius',            cats:['emotional','beginner'],       mode:'word_by_word', hlColor:'&H00FF44FF&', baseColor:'&H00FFFFFF&', outline:3.0, shadow:2, borderStyle:1 },
    { key:'wbw_putih_xl',        name:'Word×Word Putih XL',   desc:'Putih jumbo satu kata, maksimal impak',    cats:['viral_quote','emotional'],    mode:'word_by_word', hlColor:'&H00FFFFFF&', baseColor:'&H00DDDDDD&', outline:4.5, shadow:0, borderStyle:1 },
    { key:'wbw_cyan',            name:'Word×Word Cyan',       desc:'Cyan satu kata, fresh & energik',          cats:['beginner','viral_quote'],     mode:'word_by_word', hlColor:'&H00FFFF00&', baseColor:'&H00FFFFFF&', outline:3.0, shadow:3, borderStyle:1 },
    { key:'wbw_hijau_tua',       name:'Word×Word Hijau Islam',desc:'Hijau tua per kata, kajian Islam',         cats:['quran_hadith','knowledge'],   mode:'word_by_word', hlColor:'&H0033CC00&', baseColor:'&H00AAAAAA&', outline:3.0, shadow:3, borderStyle:1 },
    { key:'wbw_box_hitam',       name:'Word×Word Box Hitam',  desc:'Satu kata per box hitam, paling dramatis', cats:['viral_quote','emotional'],    mode:'word_by_word', hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    // KARAOKE
    { key:'karaoke_hijau',       name:'Karaoke Hijau Islam',  desc:'Abu jadi hijau saat aktif, ala lirik',     cats:['quran_hadith','knowledge'],   mode:'highlight',    hlColor:'&H0033CC00&', baseColor:'&H88AAAAAA&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'karaoke_merah',       name:'Karaoke Merah',        desc:'Abu jadi merah aktif, dramatis',           cats:['emotional','viral_quote'],    mode:'highlight',    hlColor:'&H000000FF&', baseColor:'&H88AAAAAA&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'karaoke_putih',       name:'Karaoke Putih Bersih', desc:'Gelap ke putih terang, profesional',       cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H66888888&', outline:1.8, shadow:3, borderStyle:1 },
    { key:'karaoke_emas_2',      name:'Karaoke Emas Premium', desc:'Versi premium karaoke emas berkilap',      cats:['quran_hadith','viral_quote'], mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H66999988&', outline:2.0, shadow:3, borderStyle:1 },
    // BLOK KATA
    { key:'blok_2kata',          name:'Blok 2 Kata Dramatis', desc:'2 kata besar, super fokus & impactful',    cats:['viral_quote','emotional'],    mode:'highlight',    hlColor:'&H0000FFFF&', baseColor:'&H00DDDDDD&', outline:3.5, shadow:0, borderStyle:1 },
    { key:'blok_5kata',          name:'Blok 5 Kata',          desc:'5 kata, ceramah cepat tetap terbaca',      cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:2, borderStyle:1 },
    { key:'blok_6kata',          name:'Blok 6 Kata Natural',  desc:'6 kata, terasa seperti subtitle film',     cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H0033CC00&', baseColor:'&H00FFFFFF&', outline:2.0, shadow:2, borderStyle:1 },
    // GLOW
    { key:'glow_putih',          name:'Glow Putih Soft',      desc:'Glow putih lembut, bersih & profesional',  cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00CCCCCC&', outline:0,   shadow:7, borderStyle:1 },
    { key:'glow_hijau',          name:'Glow Hijau Islami',    desc:'Glow hijau zamrud, spiritual & islami',    cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H0033CC00&', baseColor:'&H00AAAAAA&', outline:0,   shadow:7, borderStyle:1 },
    { key:'glow_merah',          name:'Glow Merah Api',       desc:'Glow merah berapi, emosional keras',       cats:['emotional','viral_quote'],    mode:'highlight',    hlColor:'&H000000FF&', baseColor:'&H00AAAAAA&', outline:0,   shadow:8, borderStyle:1 },
    { key:'glow_biru',           name:'Glow Biru Dingin',     desc:'Glow biru, tenang & intelektual',          cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H00FF8800&', baseColor:'&H00AAAAAA&', outline:0,   shadow:7, borderStyle:1 },
    { key:'glow_emas_2',         name:'Glow Emas Double',     desc:'Emas dengan glow dobel, paling mewah',     cats:['quran_hadith','viral_quote'], mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00BBAA88&', outline:0,   shadow:9, borderStyle:1 },
    // OUTLINE
    { key:'outline_sangat_tebal',name:'Outline Sangat Tebal', desc:'Outline 5px, terbaca di background apapun',cats:['knowledge','viral_quote'],    mode:'highlight',    hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:5.0, shadow:0, borderStyle:1 },
    { key:'outline_hijau',       name:'Outline Hijau Islam',  desc:'Outline hijau Islam, unik & khas',         cats:['quran_hadith','knowledge'],   mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00FFFFFF&', outline:3.5, shadow:2, borderStyle:1 },
    { key:'outline_emas',        name:'Outline Emas Premium', desc:'Outline emas, terasa premium & mewah',     cats:['quran_hadith','viral_quote'], mode:'highlight',    hlColor:'&H0000D4FF&', baseColor:'&H00FFFFFF&', outline:3.5, shadow:3, borderStyle:1 },
    { key:'outline_merah',       name:'Outline Merah Tegas',  desc:'Outline merah, peringatan keras',          cats:['emotional','viral_quote'],    mode:'highlight',    hlColor:'&H000000FF&', baseColor:'&H00FFFFFF&', outline:3.5, shadow:0, borderStyle:1 },
    // POSISI
    { key:'tengah_putih',        name:'Tengah Sinema Putih',  desc:'Subtitle tengah layar, ala film sinema',   cats:['emotional','quran_hadith'],   mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00CCCCCC&', outline:2.5, shadow:4, borderStyle:1 },
    { key:'tengah_emas_sinema',  name:'Tengah Emas Epik',     desc:'Emas di tengah, ala film Islam epik',      cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H0000D4FF&', baseColor:'&H00AAAAAA&', outline:3.0, shadow:5, borderStyle:1 },
    { key:'atas_putih',          name:'Atas Layar Putih',     desc:'Subtitle di atas layar',                   cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00DDDDDD&', outline:2.5, shadow:3, borderStyle:1 },
    { key:'atas_kuning',         name:'Atas Layar Kuning',    desc:'Hormozi kuning di atas, beda & viral',     cats:['viral_quote','knowledge'],    mode:'highlight',    hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:0, borderStyle:1 },
    // CINEMATIC
    { key:'cinematic_hitam',     name:'Cinematic Box Hitam',  desc:'Putih di box hitam penuh, ala dokumenter', cats:['emotional','quran_hadith'],   mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00CCCCCC&', outline:0,   shadow:0, borderStyle:3 },
    { key:'cinematic_subtitle',  name:'Cinematic Film',       desc:'Gaya subtitle bioskop, italic tipis',      cats:['knowledge','emotional'],      mode:'highlight',    hlColor:'&H00FFFF88&', baseColor:'&H00FFFFFF&', outline:1.5, shadow:1, borderStyle:1 },
    { key:'cinematic_sepia',     name:'Cinematic Sepia',      desc:'Sepia hangat, kesan klasik & nostalgia',   cats:['emotional','quran_hadith'],   mode:'highlight',    hlColor:'&H0088CCFF&', baseColor:'&H00BBDDFF&', outline:2.0, shadow:3, borderStyle:1 },
    // QURAN/ISLAMI
    { key:'quran_emas_besar',    name:'Quran Emas Besar',     desc:'Emas jumbo untuk ayat Al-Quran',           cats:['quran_hadith'],               mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00CCCCAA&', outline:3.0, shadow:4, borderStyle:1 },
    { key:'quran_hijau_zamrud',  name:'Quran Hijau Zamrud',   desc:'Hijau zamrud mewah, kajian kitab',         cats:['quran_hadith','knowledge'],   mode:'highlight',    hlColor:'&H0022DD44&', baseColor:'&H00AACCAA&', outline:2.5, shadow:3, borderStyle:1 },
    { key:'quran_putih_biru',    name:'Quran Putih-Biru Suci',desc:'Putih ke biru langit, suci & damai',       cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H00FFCCAA&', baseColor:'&H00DDDDFF&', outline:2.5, shadow:3, borderStyle:1 },
    { key:'hadits_tegas',        name:'Hadits Tegas H-P',     desc:'Bold bersih khusus hadits',                cats:['quran_hadith','knowledge'],   mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00EEEEEE&', outline:0,   shadow:0, borderStyle:3 },
    // PLATFORM
    { key:'tiktok_trendy',       name:'TikTok Trendy 2025',   desc:'Style paling viral di TikTok',             cats:['viral_quote','beginner'],     mode:'word_by_word', hlColor:'&H00FFFF00&', baseColor:'&H00FFFFFF&', outline:3.0, shadow:0, borderStyle:1 },
    { key:'reels_modern',        name:'Instagram Reels Modern',desc:'Clean modern ala konten Instagram',        cats:['viral_quote','beginner'],     mode:'highlight',    hlColor:'&H00FF88FF&', baseColor:'&H00FFFFFF&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'shorts_bold',         name:'YouTube Shorts Bold',  desc:'Optimized untuk YouTube Shorts',           cats:['viral_quote','knowledge'],    mode:'highlight',    hlColor:'&H000000FF&', baseColor:'&H00FFFFFF&', outline:3.5, shadow:2, borderStyle:1 },
    { key:'vlog_kuning',         name:'Vlog Kuning Ceria',    desc:'Casual kuning, konten edukatif santai',    cats:['beginner','viral_quote'],     mode:'highlight',    hlColor:'&H0000EEFF&', baseColor:'&H00FFFFFF&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'vlog_pink',           name:'Vlog Pink Remaja',     desc:'Pink manis, konten muda & relatable',      cats:['beginner','emotional'],       mode:'highlight',    hlColor:'&H00CC44FF&', baseColor:'&H00FFFFFF&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'vlog_oranye',         name:'Vlog Oranye Hangat',   desc:'Oranye cerah, hangat & ramah',             cats:['beginner','emotional'],       mode:'highlight',    hlColor:'&H000055FF&', baseColor:'&H00FFFFFF&', outline:2.0, shadow:2, borderStyle:1 },
    // SPECIAL
    { key:'minimalis_tipis',     name:'Minimalis Tipis Elegan',desc:'Font tipis tidak bold, elegan & dewasa',   cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00DDDDDD&', outline:1.5, shadow:2, borderStyle:1 },
    { key:'minimalis_cream',     name:'Minimalis Cream Hangat',desc:'Cream warm tone, nyaman di mata',          cats:['knowledge','emotional'],      mode:'highlight',    hlColor:'&H00DDEEFF&', baseColor:'&H00BBCCEE&', outline:1.5, shadow:2, borderStyle:1 },
    { key:'military_green',      name:'Military Green',       desc:'Hijau tua military, gagah',                cats:['knowledge','viral_quote'],    mode:'highlight',    hlColor:'&H0044AA44&', baseColor:'&H00AABBAA&', outline:3.0, shadow:2, borderStyle:1 },
    { key:'typewriter',          name:'Typewriter Klasik',    desc:'Gaya mesin ketik, satu kata per tampil',   cats:['knowledge','viral_quote'],    mode:'word_by_word', hlColor:'&H00FFFFFF&', baseColor:'&H00DDDDDD&', outline:1.5, shadow:0, borderStyle:1 },
    { key:'dakwah_bijak',        name:'Dakwah Bijak Italic',  desc:'Italic elegan emas, nasihat & hikmah',     cats:['emotional','quran_hadith'],   mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00DDDDAA&', outline:1.5, shadow:4, borderStyle:1 },
    { key:'motivasi_merah',      name:'Motivasi Merah Membara',desc:'Merah per kata, momen motivasi keras',     cats:['emotional','viral_quote'],    mode:'word_by_word', hlColor:'&H002222FF&', baseColor:'&H00FFFFFF&', outline:3.0, shadow:3, borderStyle:1 },
    { key:'tausiyah_lembut',     name:'Tausiyah Lembut',      desc:'Hijau muda italic, nasehat hati',          cats:['emotional','beginner'],       mode:'highlight',    hlColor:'&H0088FF88&', baseColor:'&H00CCEECC&', outline:1.5, shadow:3, borderStyle:1 },
    { key:'podcast_clean',       name:'Podcast Clean 5-Kata', desc:'Bersih 5 kata, ideal ceramah panjang',     cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H0066FFFF&', baseColor:'&H00FFFFFF&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'podcast_dark',        name:'Podcast Dark Mode',    desc:'Gelap elegan, konten malam hari',          cats:['knowledge','emotional'],      mode:'highlight',    hlColor:'&H00CCCCCC&', baseColor:'&H00888888&', outline:0,   shadow:0, borderStyle:3 },
    { key:'futuristik_dark',     name:'Futuristik Dark',      desc:'Latar gelap cyan futuristik',              cats:['viral_quote','beginner'],     mode:'highlight',    hlColor:'&H00EEFF00&', baseColor:'&H00888888&', outline:0,   shadow:5, borderStyle:3 },
    { key:'elegan_emas_italic',  name:'Elegan Emas Italic',   desc:'Italic emas tipis, paling elegan',         cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00AABB88&', outline:1.5, shadow:5, borderStyle:1 },
    { key:'bold_putih_polos',    name:'Bold Putih Polos',     desc:'Putih bold tanpa efek, simpel & kuat',     cats:['knowledge','viral_quote'],    mode:'no_highlight', hlColor:'&H00FFFFFF&', baseColor:'&H00FFFFFF&', outline:3.0, shadow:0, borderStyle:1 },
    { key:'hijau_kontras_max',   name:'Hijau-Putih Kontras',  desc:'Kontras maksimal, paling mudah dibaca',    cats:['knowledge','quran_hadith'],   mode:'highlight',    hlColor:'&H0000BB00&', baseColor:'&H00FFFFFF&', outline:3.0, shadow:2, borderStyle:1 },
    { key:'shadow_biru',         name:'Shadow Biru Dramatis', desc:'Shadow biru tebal, dingin & mendalam',     cats:['emotional','knowledge'],      mode:'highlight',    hlColor:'&H00FF8800&', baseColor:'&H00FFFFFF&', outline:0,   shadow:7, borderStyle:1 },
    { key:'retro_vintage',       name:'Retro Vintage',        desc:'Kuning tua retro, klasik & berkarakter',   cats:['viral_quote','beginner'],     mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00AAAAFF&', outline:2.5, shadow:3, borderStyle:1 },
    // ── BATCH 4: 50 Style Baru ───────────────────────────────────────────
    // GRADIENT
    { key:'gradient_merah_kuning', name:'Gradient Merah-Kuning',  desc:'Panas membara, urgensi & peringatan',      cats:['emotional','viral_quote'],    mode:'highlight',    hlColor:'&H000000FF&', baseColor:'&H0000AAFF&', outline:3.0, shadow:3, borderStyle:1 },
    { key:'gradient_biru_ungu',    name:'Gradient Biru-Ungu',     desc:'Elegan cool, konten modern premium',       cats:['viral_quote','beginner'],     mode:'highlight',    hlColor:'&H00FF4444&', baseColor:'&H00FFAAFF&', outline:2.5, shadow:4, borderStyle:1 },
    { key:'gradient_hijau_teal',   name:'Gradient Hijau-Teal',    desc:'Segar & natural, Islami muda',             cats:['quran_hadith','beginner'],    mode:'highlight',    hlColor:'&H0000FF88&', baseColor:'&H00DDFFDD&', outline:2.5, shadow:3, borderStyle:1 },
    { key:'gold_silver',           name:'Gold & Silver',          desc:'Emas dan perak bergantian, super mewah',   cats:['quran_hadith','viral_quote'], mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00CCCCCC&', outline:3.0, shadow:5, borderStyle:1 },
    // DUAL TONE
    { key:'dual_hijau_putih',      name:'Dual Hijau-Putih',       desc:'Hijau & putih kontras tinggi, clean Islam',cats:['quran_hadith','knowledge'],   mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H0099FF99&', outline:2.5, shadow:2, borderStyle:1 },
    { key:'dual_merah_putih',      name:'Dual Merah-Putih',       desc:'Merah & putih kontras, tegas',             cats:['emotional','viral_quote'],    mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00FF9999&', outline:2.5, shadow:2, borderStyle:1 },
    { key:'dual_emas_hitam',       name:'Dual Emas-Hitam',        desc:'Emas di hitam, paling elegan & premium',   cats:['quran_hadith','viral_quote'], mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00888866&', outline:0,   shadow:6, borderStyle:1 },
    { key:'dual_cyan_hitam',       name:'Dual Cyan-Hitam',        desc:'Cyan cerah di gelap, hacker aesthetic',    cats:['viral_quote','beginner'],     mode:'highlight',    hlColor:'&H00FFFF00&', baseColor:'&H00888888&', outline:0,   shadow:6, borderStyle:3 },
    // SHADOW EKSTREM
    { key:'shadow_emas_tebal',     name:'Shadow Emas Tebal',      desc:'Shadow emas sangat tebal, mewah & dalam',  cats:['quran_hadith','viral_quote'], mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00DDDDAA&', outline:0,   shadow:10, borderStyle:1 },
    { key:'shadow_hijau_deep',     name:'Shadow Hijau Deep',      desc:'Shadow hijau dalam, spiritual & syahdu',   cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H0033CC00&', baseColor:'&H00AAAAAA&', outline:0,   shadow:9, borderStyle:1 },
    { key:'shadow_merah_inferno',  name:'Shadow Merah Inferno',   desc:'Shadow merah api, paling dramatis',        cats:['emotional','viral_quote'],    mode:'highlight',    hlColor:'&H000000FF&', baseColor:'&H00CCCCCC&', outline:0,   shadow:10, borderStyle:1 },
    { key:'shadow_ungu_mystic',    name:'Shadow Ungu Mystic',     desc:'Shadow ungu misterius, seperti sihir',     cats:['emotional','beginner'],       mode:'highlight',    hlColor:'&H00FF88FF&', baseColor:'&H00DDDDFF&', outline:0,   shadow:9, borderStyle:1 },
    // BOX ADVANCED
    { key:'box_hijau_neon',        name:'Box Hijau Neon',         desc:'Box hijau neon gelap, unik & khas',        cats:['viral_quote','quran_hadith'], mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00AAFFAA&', outline:0,   shadow:0, borderStyle:3 },
    { key:'box_oranye',            name:'Box Oranye Energik',     desc:'Box oranye muda, ceria & menarik',         cats:['beginner','viral_quote'],     mode:'highlight',    hlColor:'&H000055FF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    { key:'box_abu_gelap',         name:'Box Abu Gelap',          desc:'Box abu gelap, clean dark mode',           cats:['knowledge','emotional'],      mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00CCCCCC&', outline:0,   shadow:0, borderStyle:3 },
    { key:'box_merah_neon',        name:'Box Merah Neon',         desc:'Box merah neon gelap, sangat mencolok',    cats:['emotional','viral_quote'],    mode:'highlight',    hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    { key:'box_ungu_royal',        name:'Box Ungu Royal',         desc:'Box ungu kerajaan, paling mewah',          cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00FFDDFF&', outline:0,   shadow:0, borderStyle:3 },
    // MULTI KATA EKSTREM
    { key:'satu_kata_raksasa',     name:'1 Kata Raksasa',         desc:'Satu kata sangat besar, ultra dramatis',   cats:['viral_quote','emotional'],    mode:'word_by_word', hlColor:'&H00FFFFFF&', baseColor:'&H00DDDDDD&', outline:5.0, shadow:0, borderStyle:1 },
    { key:'dua_kata_kotak',        name:'2 Kata + Box Hitam',     desc:'2 kata di box hitam, sangat bold',         cats:['viral_quote','emotional'],    mode:'highlight',    hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    { key:'tujuh_kata',            name:'7 Kata Per Baris',       desc:'7 kata, sangat alami seperti baca teks',   cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H0066FFFF&', baseColor:'&H00FFFFFF&', outline:1.8, shadow:1, borderStyle:1 },
    // ITALIC
    { key:'italic_putih',          name:'Italic Putih Bersih',    desc:'Italic putih, gaya narasi film',           cats:['emotional','knowledge'],      mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00DDDDDD&', outline:2.0, shadow:3, borderStyle:1 },
    { key:'italic_emas',           name:'Italic Emas Mewah',      desc:'Italic emas, paling mewah untuk nasihat',  cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00AABB88&', outline:1.8, shadow:5, borderStyle:1 },
    { key:'italic_hijau',          name:'Italic Hijau Damai',     desc:'Italic hijau, damai & menenangkan',        cats:['quran_hadith','beginner'],    mode:'highlight',    hlColor:'&H0055EE55&', baseColor:'&H00AACCAA&', outline:1.8, shadow:3, borderStyle:1 },
    { key:'italic_merah',          name:'Italic Merah Tegas',     desc:'Italic merah, peringatan tapi elegan',     cats:['emotional','viral_quote'],    mode:'highlight',    hlColor:'&H000000FF&', baseColor:'&H00FFCCCC&', outline:2.0, shadow:3, borderStyle:1 },
    // POSISI
    { key:'kiri_putih',            name:'Rata Kiri Putih',        desc:'Teks rata kiri, gaya berita & dokumenter', cats:['knowledge','emotional'],      mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00DDDDDD&', outline:2.5, shadow:3, borderStyle:1 },
    { key:'kiri_kuning',           name:'Rata Kiri Kuning',       desc:'Hormozi kuning rata kiri, unik & viral',   cats:['viral_quote','knowledge'],    mode:'highlight',    hlColor:'&H0000FFFF&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:0, borderStyle:1 },
    // FROSTED
    { key:'frosted_putih',         name:'Frosted Glass Putih',    desc:'Efek kaca buram putih, sangat modern',     cats:['beginner','knowledge'],       mode:'highlight',    hlColor:'&H00111111&', baseColor:'&H00444444&', outline:0,   shadow:0, borderStyle:3 },
    { key:'frosted_gelap',         name:'Frosted Glass Gelap',    desc:'Efek kaca gelap, konten premium malam',    cats:['knowledge','emotional'],      mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00BBBBBB&', outline:0,   shadow:0, borderStyle:3 },
    // WBW ADVANCED
    { key:'wbw_box_emas',          name:'WxW Box Emas',           desc:'Satu kata per box emas, sangat mewah',     cats:['quran_hadith','viral_quote'], mode:'word_by_word', hlColor:'&H0000CCFF&', baseColor:'&H00CCCCAA&', outline:0,   shadow:0, borderStyle:3 },
    { key:'wbw_box_merah',         name:'WxW Box Merah',          desc:'Satu kata per box merah, dramatis total',  cats:['emotional','viral_quote'],    mode:'word_by_word', hlColor:'&H000000FF&', baseColor:'&H00FFFFFF&', outline:0,   shadow:0, borderStyle:3 },
    { key:'wbw_neon_kuning',       name:'WxW Neon Kuning',        desc:'Satu kata neon kuning, paling mencolok',   cats:['viral_quote','beginner'],     mode:'word_by_word', hlColor:'&H00FFFF00&', baseColor:'&H00888888&', outline:3.0, shadow:7, borderStyle:1 },
    { key:'wbw_glow_putih',        name:'WxW Glow Putih',         desc:'Satu kata dengan glow putih intens',       cats:['emotional','viral_quote'],    mode:'word_by_word', hlColor:'&H00FFFFFF&', baseColor:'&H00AAAAAA&', outline:0,   shadow:10, borderStyle:1 },
    // ISLAMI KHUSUS
    { key:'subhanallah',           name:'Subhanallah Style',      desc:'Putih suci bercahaya, dzikir & tasbih',    cats:['quran_hadith','emotional'],   mode:'word_by_word', hlColor:'&H00FFFFFF&', baseColor:'&H00DDDDFF&', outline:2.5, shadow:7, borderStyle:1 },
    { key:'asmaul_husna',          name:'Asmaul Husna',           desc:'Emas mulia, penyebutan nama Allah',        cats:['quran_hadith'],               mode:'word_by_word', hlColor:'&H0000EEFF&', baseColor:'&H00CCBB88&', outline:3.0, shadow:5, borderStyle:1 },
    { key:'khutbah_jumat',         name:'Khutbah Jumat',          desc:'Hitam putih tegas, khusus konten khutbah', cats:['quran_hadith','knowledge'],   mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00EEEEEE&', outline:0,   shadow:0, borderStyle:3 },
    { key:'ramadan_emas',          name:'Ramadan Emas',           desc:'Emas festif untuk konten Ramadan & Eid',   cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00CCBB88&', outline:2.5, shadow:5, borderStyle:1 },
    { key:'hijriyah_perak',        name:'Hijriyah Perak',         desc:'Perak elegan, sejarah & kalender Islam',   cats:['quran_hadith','knowledge'],   mode:'highlight',    hlColor:'&H00DDDDDD&', baseColor:'&H00AAAAAA&', outline:2.5, shadow:4, borderStyle:1 },
    // PLATFORM ADVANCED
    { key:'youtube_end_screen',    name:'YouTube End Screen',     desc:'Bold besar untuk intro/outro YouTube',     cats:['viral_quote','knowledge'],    mode:'highlight',    hlColor:'&H000000FF&', baseColor:'&H00FFFFFF&', outline:4.0, shadow:2, borderStyle:1 },
    { key:'instagram_story',       name:'Instagram Story',        desc:'Minimalis cantik, Instagram Story',        cats:['beginner','emotional'],       mode:'highlight',    hlColor:'&H00FF66BB&', baseColor:'&H00FFFFFF&', outline:1.8, shadow:2, borderStyle:1 },
    { key:'facebook_dakwah',       name:'Facebook Dakwah',        desc:'Besar & jelas, optimal Facebook viewer',   cats:['knowledge','quran_hadith'],   mode:'highlight',    hlColor:'&H0033CC00&', baseColor:'&H00FFFFFF&', outline:3.0, shadow:2, borderStyle:1 },
    { key:'twitter_x_bold',        name:'Twitter/X Bold',         desc:'Tajam & ringkas, gaya Twitter/X post',     cats:['viral_quote','knowledge'],    mode:'highlight',    hlColor:'&H00EEEEFF&', baseColor:'&H00FFFFFF&', outline:2.5, shadow:0, borderStyle:1 },
    // AURA
    { key:'aura_putih',            name:'Aura Putih Suci',        desc:'Cahaya putih aura, spiritual & khidmat',   cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H66FFFFFF&', outline:0,   shadow:12, borderStyle:1 },
    { key:'aura_hijau',            name:'Aura Hijau Langit',      desc:'Aura hijau langit, surga & rahmat',        cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H0033CC00&', baseColor:'&H6688FF88&', outline:0,   shadow:11, borderStyle:1 },
    { key:'aura_emas',             name:'Aura Emas Surgawi',      desc:'Aura emas bercahaya, konten akhirat',      cats:['quran_hadith','viral_quote'], mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H66CCCCAA&', outline:0,   shadow:11, borderStyle:1 },
    // KARAOKE ADVANCED
    { key:'karaoke_ungu',          name:'Karaoke Ungu',           desc:'Abu jadi ungu aktif, misterius & unik',    cats:['emotional','beginner'],       mode:'highlight',    hlColor:'&H00FF44FF&', baseColor:'&H88AAAAAA&', outline:2.0, shadow:2, borderStyle:1 },
    { key:'karaoke_cyan',          name:'Karaoke Cyan Fresh',     desc:'Abu jadi cyan fresh, modern & energik',    cats:['beginner','viral_quote'],     mode:'highlight',    hlColor:'&H00FFFF00&', baseColor:'&H88AAAAAA&', outline:2.0, shadow:3, borderStyle:1 },
    { key:'karaoke_oranye',        name:'Karaoke Oranye',         desc:'Abu jadi oranye, hangat & semangat',       cats:['beginner','emotional'],       mode:'highlight',    hlColor:'&H000055FF&', baseColor:'&H88AAAAAA&', outline:2.0, shadow:2, borderStyle:1 },
    // MINIMALIS ADVANCED
    { key:'minimalis_biru',        name:'Minimalis Biru Tenang',  desc:'Biru tenang, cocok topik ilmu & sains',    cats:['knowledge','beginner'],       mode:'highlight',    hlColor:'&H00AABBFF&', baseColor:'&H00CCDDFF&', outline:1.5, shadow:2, borderStyle:1 },
    { key:'minimalis_coklat',      name:'Minimalis Coklat Earthy',desc:'Coklat earth tone, hangat & membumi',      cats:['knowledge','emotional'],      mode:'highlight',    hlColor:'&H0099CCFF&', baseColor:'&H00BBDDFF&', outline:1.5, shadow:2, borderStyle:1 },
    { key:'minimalis_hitam',       name:'Minimalis Hitam Bold',   desc:'Hitam bold simpel, keterbacaan max',       cats:['knowledge','viral_quote'],    mode:'highlight',    hlColor:'&H00111111&', baseColor:'&H00444444&', outline:0,   shadow:0, borderStyle:3 },
    // KOMBINASI UNIK
    { key:'neon_box_ungu',         name:'Neon Box Ungu',          desc:'Teks neon di box ungu gelap, sangat viral',cats:['viral_quote','beginner'],     mode:'highlight',    hlColor:'&H00FFFFFF&', baseColor:'&H00FFAAFF&', outline:0,   shadow:5, borderStyle:3 },
    { key:'emas_box_hitam',        name:'Emas di Box Hitam',      desc:'Teks emas di box hitam, paling premium',   cats:['quran_hadith','viral_quote'], mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00CCBB88&', outline:0,   shadow:0, borderStyle:3 },
    { key:'putih_outline_emas',    name:'Putih + Outline Emas',   desc:'Teks putih outline emas, elegan banget',   cats:['quran_hadith','emotional'],   mode:'highlight',    hlColor:'&H0000CCFF&', baseColor:'&H00FFFFFF&', outline:4.0, shadow:3, borderStyle:1 },
    { key:'wbw_tengah_emas',       name:'WxW Tengah Emas',        desc:'Satu kata emas di tengah layar, epik',     cats:['quran_hadith','viral_quote'], mode:'word_by_word', hlColor:'&H0000CCFF&', baseColor:'&H00AAAAAA&', outline:3.5, shadow:6, borderStyle:1 },
    { key:'bold_hijau_xl',         name:'Bold Hijau XL',          desc:'Hijau besar extra bold, dakwah paling impak',cats:['quran_hadith','viral_quote'],mode:'highlight',   hlColor:'&H0022DD22&', baseColor:'&H00FFFFFF&', outline:3.5, shadow:3, borderStyle:1 },
  ]
}

function updateWhisperInfo(model) {
  const info = {
    'tiny':     '⚡ tiny: 75MB · Tercepat, kurang akurat untuk ceramah Arab-Indonesia',
    'base':     '✅ base: 145MB · Cepat, cocok audio jernih',
    'small':    '✅ small: 490MB · Seimbang cepat & akurat — Rekomendasi untuk ceramah',
    'medium':   '🎯 medium: 1.5GB · Sangat akurat, bagus untuk istilah Arab & logat',
    'turbo':    '🚀 turbo: 1.6GB · Cepat + akurat — Model terbaru OpenAI',
    'large-v3': '🏆 large-v3: 3GB · Terbaik, butuh RAM 6GB+',
  }
  const el = document.getElementById('whisper-info')
  if (el) el.innerHTML = info[model] || model
}

function initAboutPage() {
  // Tampilkan iklan di halaman Tentang
  AdManager.show('about', 'ad-banner-about')

  const donate = document.getElementById('btn-donate')
  if (donate) donate.onclick = () =>
    window.app.openUrl('https://saweria.co')

  const github = document.getElementById('btn-github')
  if (github) github.onclick = () =>
    window.app.openUrl('https://github.com')

  const feedback = document.getElementById('btn-feedback')
  if (feedback) feedback.onclick = () =>
    window.app.openUrl('mailto:feedback@mahiraclipper.id')

  const report = document.getElementById('btn-report')
  if (report) report.onclick = () =>
    window.app.openUrl('https://github.com')
}

window.deleteProject     = deleteProject
window.copyKey           = copyKey
window.updateWhisperInfo = updateWhisperInfo
window.openProjectModal  = openProjectModal
window.openProjectFolder = openProjectFolder
window.closeModal        = closeModal
window.openClipFile      = openClipFile
