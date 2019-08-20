import Database from "../models/database";
import {ipcMain} from 'electron'
import log from 'electron-log'


export default class Processes {

    constructor() {
        ipcMain.on('get-processes-data', async (event: any, arg: any) => {
            event.returnValue = await this.getProcessesData();
        });

        ipcMain.on('get-windows-data', async (event: any, arg: any) => {
            event.returnValue = await this.getProcessesData();
        });
    }

    async getProcessesData() {
        try {
            let results: any = await Database.db.all(`
                SELECT path,
                       SUM(difference) AS time,
                       process_id,
                       pt.type,
                       pt.color
                FROM heartbeats AS hb
                         JOIN
                         (SELECT start_time, end_time - start_time AS difference FROM heartbeats) d
                         ON
                             d.start_time = hb.start_time
                         LEFT JOIN
                     processes p on hb.process_id = p.id
                         LEFT JOIN
                     productivity_type pt on p.type_str = pt.type
                WHERE hb.idle = FALSE AND path NOT NULL AND path <> ''
                GROUP BY process_id
                ORDER BY SUM(difference) DESC`);

            for (let result of results) {
                if (result.name == undefined) {
                    let regex: RegExp;
                    if (process.platform === 'win32') {
                        regex = /\\(.+\\)*(.+)\./;
                    } else {
                        regex = /\/(?:,+\/\/)*(.+)\/(.*)/
                    }

                    if (result.path.search(regex) < 0) {
                        log.warn(result.path);
                        continue;
                    }

                    result.name = result.path.match(regex)[2];
                }
            }

            return results;
        } catch (e) {
            log.error(e);
        }
    }
}
