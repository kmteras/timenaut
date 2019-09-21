import Database from "@/models/database";
import {ipcMain} from 'electron'
import log from 'electron-log'


export default class Settings {
    private static settings: { [key: string]: string } = {};

    public static async init() {
        ipcMain.on('get-setting', async (event: Event, key: string) => {
            // @ts-ignore
            event.returnValue = await Settings.getSetting(key);
        });

        ipcMain.on('set-setting', async (event: Event, key: string, value: string) => {
            // @ts-ignore
            event.returnValue = await Settings.setSetting(key, value);
        });

        await this.initSettingNum('heartbeatPollTime', 10);
        await this.initSettingNum('heartbeatIdleTime', 300);
    }

    public static async getSetting(key: string): Promise<string | null> {
        if (key in this.settings) {
            return this.settings[key];
        }

        const sql = `SELECT value
                     FROM settings
                     WHERE key = ?
                       AND metadata = FALSE`;
        let value = await Database.db.one(sql, [key]);
        if (value === undefined) {
            value = null;
        } else {
            value = value['value'];
        }
        this.settings[key] = value;
        log.debug(`Fetched setting ${key} with value ${value}`);
        return value;
    }

    public static async setSetting(key: string, value: string): Promise<string> {

        const sql = `INSERT INTO settings(key, value)
                     VALUES (?, ?)
                     ON CONFLICT(key) DO UPDATE SET value=?
                     WHERE key = ?`;
        await Database.db.run(sql, [key, value, value, key]);
        this.settings[key] = value;
        log.debug(`Set setting ${key} as ${value}`);
        return value;
    }

    private static async initSetting(key: string, defaultValue: string): Promise<string> {
        let value = await this.getSetting(key);

        if (value === null) {
            return await this.setSetting(key, defaultValue);
        } else {
            return value;
        }
    }

    private static async initSettingNum(key: string, defaultValue: number): Promise<number> {
        return Number.parseInt(await this.initSetting(key, defaultValue.toString()));
    }

    public static getPollTime(): number {
        return Number.parseInt(Settings.settings['heartbeatPollTime']);
    }

    public static getIdleTime(): number {
        return Number.parseInt(Settings.settings['heartbeatIdleTime']);
    }
}
