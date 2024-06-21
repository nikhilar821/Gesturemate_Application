const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')

function createWindow() {
  const mainWindow = new BrowserWindow({
    icon: 'C:/Users/Nikhila/electro/electro/icon.png',
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
    },
  })

  mainWindow.loadFile('src/index.html')
  mainWindow.setMenuBarVisibility(false);
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

ipcMain.on('run-python-script', (event, args) => {
  const { spawn } = require('child_process')
  const pythonProcess = spawn('C:/Users/Nikhila/electro/electro/src/finale.exe', args)

  pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString())
  })

  pythonProcess.stderr.on('data', (data) => {
    console.error(data.toString())
  })

  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`)
  })
})