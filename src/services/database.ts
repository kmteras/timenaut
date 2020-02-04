import sqlite3 from 'sqlite3';
import {app} from 'electron'
import * as path from 'path';
import log from 'electron-log';
import databaseInit from '@/services/database_init';

type ParamTypes = number | string | Buffer | boolean | null | undefined;

export default class Database {
    db?: sqlite3.Database;
    static db: Database;

    constructor() {
        Database.db = this;
    }

    async connect(test: boolean = false) {
        let databaseFileName = process.env.WEBPACK_DEV_SERVER_URL ? 'timenaut_dev.dat' : 'timenaut.dat';

        let databaseFile;

        if (test) {
            databaseFile = ":memory:";
            log.info("Using memory database");
        } else {
            databaseFile = path.join(app.getPath('userData'), databaseFileName);
            log.info(`Opening database at ${databaseFile}`);
        }

        this.db = await this.openDatabase(databaseFile);
        log.info("Database opened");
        log.debug(`Database ${this.db}`);
        await Database.exec('PRAGMA journal_mode = WAL');
        await Database.exec('PRAGMA synchronous = 1');
        await Database.exec('PRAGMA foreign_keys = ON');
    }

    async openDatabase(databaseFile: string): Promise<sqlite3.Database> {
        return new Promise(((resolve, reject) => {
            const db = new sqlite3.Database(databaseFile, (err: (Error | null)) => {
                if (err) {
                    reject(err);
                }
                resolve(db);
            });
        }))
    }

    async update(): Promise<void> {
        return new Promise(((resolve, reject) => {
            Database.db.db!.exec(databaseInit, (err: Error | null) => {
                if (err) {
                    reject(err)
                }
                resolve();
            });
        }));
    }

    static async all(sql: string, params?: ParamTypes[]): Promise<any[]> {
        if (this.db === undefined) {
            throw Error("Not connected to the database");
        }

        return new Promise(((resolve, reject) => {
            params = this.convertTypes(params);

            Database.db.db!.all(sql, params, (err: Error | null, row: any[]) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        }));
    }

    static async one(sql: string, params: ParamTypes[] = []): Promise<any> {
        if (this.db === undefined) {
            throw Error("Not connected to the database");
        }

        return new Promise(((resolve, reject) => {
            params = this.convertTypes(params);

            Database.db.db!.get(sql, params, (err: Error | null, row: any) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        }));
    }

    static async run(sql: string, params?: ParamTypes[]): Promise<void> {
        if (this.db === undefined) {
            throw Error("Not connected to the database");
        }

        return new Promise(((resolve, reject) => {
            params = this.convertTypes(params);

            Database.db.db!.run(sql, params, (err: Error | null) => {
                if (err) {
                    reject(err);
                }
                resolve();
            });
        }));
    }

    static async exec(sql: string): Promise<void> {
        if (this.db === undefined) {
            throw Error("Not connected to the database");
        }

        return new Promise(((resolve, reject) => {
            Database.db.db!.exec(sql, (err: Error | null) => {
                if (err) {
                    reject(err);
                }
                resolve();
            });
        }));
    }

    private static convertTypes(params: ParamTypes[] = []): ParamTypes[] {
        if (params !== undefined) {
            for (let i = 0; i < params.length; i++) {
                let param = params[i];
                if (typeof param == "boolean") {
                    params[i] = param ? 1 : 0;
                }
            }
        }
        return params;
    }
}
