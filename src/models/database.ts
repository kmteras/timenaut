import * as sqlite3 from 'sqlite3';
import {app, BrowserWindow, ipcMain, protocol} from 'electron'
import * as path from 'path';


export default class Database {
    db?: sqlite3.Database;
    static db: Database;

    constructor() {
        Database.db = this;
    }

    async connect() {
        return new Promise((resolve, reject) => {
            this.db = new sqlite3.Database(path.join(app.getPath('userData'), 'timechart_dev.dat'), (err) => {
                if (err) {
                    return reject(err);
                }
                console.log('Connected to the database');
                return resolve();
            })
        });
    }

    all(sql: string, params?: any) {
        return new Promise((resolve, reject) => {
            if (this.db === undefined) {
                return reject("Not connected to the database");
            }

            this.db.all(sql, params, (err, response) => {
                if (err) {
                    return reject(err);
                }
                return resolve(response);
            })
        });
    }

    run(sql: string, params?: any) {
        return new Promise((resolve, reject) => {
            if (this.db === undefined) {
                return reject("Not connected to the database");
            }

            this.db.run(sql, params);
            resolve();
        })
    }
}
