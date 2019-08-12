'use strict';

import {app, BrowserWindow, ipcMain, Menu, protocol, Tray, nativeImage} from 'electron'
import {createProtocol, installVueDevtools} from 'vue-cli-plugin-electron-builder/lib'
import Database from "./models/database";
import Timeline from "./services/timeline";
import DailyPieChart from "./services/dailyPieChart";
import Heartbeat from "./services/heartbeat";
import path from 'path';


const isDevelopment = process.env.NODE_ENV !== 'production';

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win: any;
let db: Database;
let tray: any;

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([{scheme: 'app', privileges: {secure: true, standard: true}}]);

async function createWindow() {
    // Create the browser window.
    db = new Database();
    await db.connect();
    await db.update();

    new Timeline(db);
    new DailyPieChart();

    let iconUrl = null;
    if (process.env.WEBPACK_DEV_SERVER_URL) {
        // @ts-ignore
        iconUrl = path.join(__static, 'icon_development.png');
    } else {
        // @ts-ignore
        iconUrl = path.join(__static, 'icon.png');
    }

    win = new BrowserWindow({
        width: 800, height: 600, resizable: false, webPreferences: {
            nodeIntegration: true
        },
        show: !process.env.WEBPACK_DEV_SERVER_URL,
        icon: iconUrl
    });

    let heartbeat = new Heartbeat(win);
    heartbeat.start();

    if (process.env.WEBPACK_DEV_SERVER_URL) {
        // Load the url of the dev server if in development mode
        win.loadURL(process.env.WEBPACK_DEV_SERVER_URL);
        win.showInactive();
        // if (!process.env.IS_TEST) win.webContents.openDevTools();
    } else {
        createProtocol('app');
        // Load the index.html when not in development
        win.loadURL('app://./index.html');
    }

    ipcMain.on('synchronous-message', (event: any, arg: any) => {
        event.returnValue = 'pong'
    });

    tray = new Tray(iconUrl);
    const contextMenu = Menu.buildFromTemplate([
        {
            label: 'Show/Hide', click() {
                if (win.isVisible()) {
                    win.hide();
                } else {
                    win.show();
                }
            }
        },
        {type: 'separator'},
        {
            label: 'Quit', click() {
                // @ts-ignore
                app.close = true;
                app.quit();
            }
        },
    ]);
    tray.setToolTip('Timechart');
    tray.setContextMenu(contextMenu);
    tray.setHighlightMode('always');

    win.on('close', (event: Event) => {
        // @ts-ignore
        if (!app.close) {
            win.hide();
            event.preventDefault();
        }
    });

    win.on('closed', () => {
        win = null;
    });
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', async () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (win === null) {
        await createWindow();
    }
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
    if (isDevelopment && !process.env.IS_TEST) {
        // Install Vue Devtools
        try {
            await installVueDevtools()
        } catch (e) {
            console.error('Vue Devtools failed to install:', e.toString())
        }
    }
    await createWindow();
});

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
    if (process.platform === 'win32') {
        process.on('message', data => {
            if (data === 'graceful-exit') {
                app.quit();
            }
        })
    } else {
        process.on('SIGTERM', () => {
            app.quit()
        })
    }
}
