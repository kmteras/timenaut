import * as sqlite3 from 'sqlite3';
import {app, BrowserWindow, ipcMain, protocol} from 'electron'
import * as path from 'path';


export default class Database {
    db: sqlite3.Database;
    static db: Database;

    constructor() {
        this.db = new sqlite3.Database(path.join(app.getPath('userData'), 'timechart_dev.dat'), (err) => {
             if (err) {
                 console.log(err);
                 throw err;
             }
             else {
                 console.log('Connected to the database');
                 Database.db = this;
             }
        });
    }

    all(sql: string, params?: any) {
        return new Promise((resolve, reject) => {
            this.db.all(sql, params, (err, response) => {
                if (err) {
                    reject(err);
                }
                resolve(response);
            })
        })
    }
}
