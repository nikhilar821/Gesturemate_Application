const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
    runPythonScript: () => ipcRenderer.send('run-python-script'),
})