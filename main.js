const { app, BrowserWindow, ipcMain, shell, dialog } = require('electron')
const { spawn, execSync } = require('child_process')
const path = require('path')
const fs   = require('fs')

// Semua path relatif ke root folder (tempat main.js ini berada)
const ROOT      = __dirname
const ADS_FILE   = path.join(ROOT, 'ads.json')
const RENDERER  = path.join(ROOT, 'renderer', 'index.html')
const PY_RUNNER = path.join(ROOT, 'pipeline', 'run.py')
const PROJECTS  = path.join(ROOT, 'projects')
const CFG_FILE  = path.join(ROOT, 'api_config.json')

let win = null
let activeChild = null  // track active pipeline process

// ── Window ────────────────────────────────────────────────────────────────────
function createWindow() {
  win = new BrowserWindow({
    width: 1100, height: 740,
    minWidth: 900, minHeight: 600,
    frame: false,
    backgroundColor: '#FAFAF7',
    webPreferences: {
      preload: path.join(ROOT, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    show: false,
  })
  win.loadFile(RENDERER)
  win.once('ready-to-show', () => win.show())
  win.on('closed', () => { win = null })
}

app.whenReady().then(createWindow)
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })

// ── Window controls ───────────────────────────────────────────────────────────
ipcMain.on('win-minimize', () => win?.minimize())
ipcMain.on('win-maximize', () => win?.isMaximized() ? win.unmaximize() : win.maximize())
ipcMain.on('win-close',    () => win?.close())

// ── File dialogs ──────────────────────────────────────────────────────────────
ipcMain.handle('pick-file', async () => {
  const r = await dialog.showOpenDialog(win, {
    title: 'Pilih File Video',
    filters: [{ name: 'Video', extensions: ['mp4','mkv','avi','mov','webm','m4v'] }],
    properties: ['openFile'],
  })
  return r.canceled ? null : r.filePaths[0]
})

ipcMain.on('open-folder', (_, p) => {
  if (!p) return
  const resolved = path.resolve(p)
  // Kalau final/ folder tidak ada, fallback ke parent folder
  if (fs.existsSync(resolved)) {
    shell.openPath(resolved)
  } else {
    const parent = path.dirname(resolved)
    if (fs.existsSync(parent)) shell.openPath(parent)
    else shell.openPath(PROJECTS)
  }
})

ipcMain.on('open-url', (_, u) => shell.openExternal(u))

ipcMain.on('open-projects-folder', () => {
  if (fs.existsSync(PROJECTS)) shell.openPath(PROJECTS)
})

ipcMain.on('open-clip-file', (_, p) => {
  if (p && fs.existsSync(p)) shell.openPath(p)
})

// ── Config ────────────────────────────────────────────────────────────────────
ipcMain.handle('get-config', () => {
  try { return JSON.parse(fs.readFileSync(CFG_FILE, 'utf8')) }
  catch { return {} }
})

ipcMain.handle('save-config', (_, data) => {
  let existing = {}
  try { existing = JSON.parse(fs.readFileSync(CFG_FILE, 'utf8')) } catch {}
  fs.writeFileSync(CFG_FILE, JSON.stringify(deepMerge(existing, data), null, 2), 'utf8')
  return { ok: true }
})

// ── Projects ──────────────────────────────────────────────────────────────────
ipcMain.handle('get-projects', () => {
  if (!fs.existsSync(PROJECTS)) return []
  return fs.readdirSync(PROJECTS)
    .map(id => {
      try {
        const data = JSON.parse(fs.readFileSync(path.join(PROJECTS, id, 'project.json'), 'utf8'))
        // Normalize folder path jadi absolute (fix relative path bug Windows)
        if (data.folder) data.folder = path.resolve(data.folder)
        return data
      }
      catch { return null }
    })
    .filter(Boolean)
    .sort((a, b) => (b.updated_at || '').localeCompare(a.updated_at || ''))
})

ipcMain.handle('delete-project', (_, id) => {
  const dir = path.join(PROJECTS, id)
  if (fs.existsSync(dir)) fs.rmSync(dir, { recursive: true, force: true })
  return { ok: true }
})

// ── Pipeline ──────────────────────────────────────────────────────────────────
ipcMain.on('stop-pipeline', () => {
  if (activeChild) { activeChild.kill(); activeChild = null }
})

ipcMain.on('run-pipeline', (event, cfg) => {
  // Kill previous run jika masih jalan
  if (activeChild) { activeChild.kill(); activeChild = null }

  // Cari Python yang tersedia di PATH
  const candidates = process.platform === 'win32'
    ? ['python', 'python3', 'py']
    : ['python3', 'python']

  let pyCmd = 'python'
  for (const cmd of candidates) {
    try { execSync(`${cmd} --version`, { stdio: 'ignore' }); pyCmd = cmd; break }
    catch {}
  }

  activeChild = spawn(pyCmd, [PY_RUNNER], {
    cwd: path.join(ROOT, 'pipeline'),
    stdio: ['pipe', 'pipe', 'pipe'],
    env: {
      ...process.env,
      PYTHONIOENCODING: 'utf-8',   // fix charmap error di Windows
      PYTHONUTF8: '1',             // Python 3.7+ UTF-8 mode
    },
  })

  // Kirim config ke Python via stdin (satu baris JSON)
  activeChild.stdin.write(JSON.stringify(cfg) + '\n')
  activeChild.stdin.end()

  // Stream stdout JSON lines ke renderer
  let buf = ''
  activeChild.stdout.on('data', chunk => {
    buf += chunk.toString()
    const lines = buf.split('\n')
    buf = lines.pop()
    for (const line of lines) {
      if (!line.trim()) continue
      try {
        event.sender.send('pipeline-event', JSON.parse(line))
      } catch {}
    }
  })

  activeChild.stderr.on('data', chunk => {
    const txt = chunk.toString().trim()
    if (txt) event.sender.send('pipeline-event', { event: 'log', msg: txt, level: 'warn' })
  })

  activeChild.on('exit', code => {
    if (code !== 0) event.sender.send('pipeline-event', {
      event: 'error', msg: `Pipeline berhenti (kode: ${code})`
    })
  })

  activeChild.on('error', err => {
    event.sender.send('pipeline-event', {
      event: 'error',
      msg: `Tidak bisa jalankan Python: ${err.message}\nPastikan Python ada di PATH.`
    })
  })
})

// ── Ads ──────────────────────────────────────────────────────────────────────
ipcMain.handle('get-ads', () => {
  try { return JSON.parse(fs.readFileSync(ADS_FILE, 'utf8')) }
  catch { return { settings: {}, ads: [] } }
})

// ── Helpers ───────────────────────────────────────────────────────────────────
function deepMerge(target, source) {
  const out = Object.assign({}, target)
  for (const key of Object.keys(source)) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      out[key] = deepMerge(target[key] || {}, source[key])
    } else {
      out[key] = source[key]
    }
  }
  return out
}
