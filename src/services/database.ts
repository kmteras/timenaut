import Sqlite from 'better-sqlite3';
import {app} from 'electron'
import * as path from 'path';
import log from 'electron-log';
import databaseInit from '@/services/database_init';

type ParamTypes = number | string | Buffer | boolean | null | undefined;

export default class Database {
    db?: Sqlite.Database;
    static db: Database;

    constructor() {
        Database.db = this;
    }

    async connect() {
        let option = {
            // verbose: log.debug
        };

        let databaseFileName = process.env.WEBPACK_DEV_SERVER_URL ? 'timenaut_dev.dat' : 'timenaut.dat';

        let databaseFile = path.join(app.getPath('userData'), databaseFileName);

        log.info(`Opening database at ${databaseFile}`);
        this.db = await new Sqlite(databaseFile, option);
        this.db.pragma('journal_mode = WAL');
        this.db.pragma('synchronous = 1');
        this.db.pragma('foreign_keys = ON');
    }

    async update() {
        try {
            await this.db!.exec(databaseInit);
        } catch (e) {
            throw e;
        }
    }

    all(sql: string, params?: ParamTypes[]): any[] {
        if (this.db === undefined) {
            throw Error("Not connected to the database");
        }

        params = this.convertTypes(params);

        let statement: Sqlite.Statement = this.db.prepare(sql);

        if (params) {
            return statement.all(params);
        } else {
            return statement.all();
        }
    }

    one(sql: string, params?: ParamTypes[]): any {
        if (this.db === undefined) {
            throw Error("Not connected to the database");
        }

        params = this.convertTypes(params);

        let statement: Sqlite.Statement = this.db.prepare(sql);
        if (params) {
            return statement.get(params);
        } else {
            return statement.get();
        }
    }

    run(sql: string, params?: ParamTypes[]): void {
        if (this.db === undefined) {
            throw Error("Not connected to the database");
        }

        params = this.convertTypes(params);

        try {
            let statement: Sqlite.Statement = this.db.prepare(sql);
            statement.run(params);
        } catch (e) {
            log.error(e);
        }
    }

    private convertTypes(params?: ParamTypes[]): ParamTypes[] | undefined {
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
