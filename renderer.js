const { ipcRenderer } = require('electron')
const runButton = document.getElementById('run-button')

runButton.addEventListener('click', () => {
    ipcRenderer.send('run-python-script', ['arg1', 'arg2'])
})