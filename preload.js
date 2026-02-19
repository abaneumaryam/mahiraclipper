const { contextBridge, ipcRenderer, webUtils } = require('electron')

contextBridge.exposeInMainWorld('app', {
  minimize: ()  => ipcRenderer.send('win-minimize'),
  maximize: ()  => ipcRenderer.send('win-maximize'),
  close:    ()  => ipcRenderer.send('win-close'),

  pickFile:   ()  => ipcRenderer.invoke('pick-file'),
  openFolder: (p) => ipcRenderer.send('open-folder', p),
  openProjectsFolder: () => ipcRenderer.send('open-projects-folder'),
  openClipFile: (p) => ipcRenderer.send('open-clip-file', p),
  getAds: () => ipcRenderer.invoke('get-ads'),
  openUrl:    (u) => ipcRenderer.send('open-url', u),

  getConfig:  ()  => ipcRenderer.invoke('get-config'),
  saveConfig: (d) => ipcRenderer.invoke('save-config', d),

  getProjects:   ()   => ipcRenderer.invoke('get-projects'),
  deleteProject: (id) => ipcRenderer.invoke('delete-project', id),

  runPipeline: (cfg) => ipcRenderer.send('run-pipeline', cfg),
  // Dapat path asli dari drag-drop file (Electron >= 32)
  getFilePath: (file) => {
    try { return webUtils.getPathForFile(file) }
    catch { return file.path || null }  // fallback older Electron
  },

  onPipelineEvent: (cb) => {
    const fn = (_, data) => cb(data)
    ipcRenderer.on('pipeline-event', fn)
    return () => ipcRenderer.removeListener('pipeline-event', fn)
  },
})
