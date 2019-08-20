import Database from "../models/database";
import {ipcMain} from 'electron'
import log from 'electron-log'


export default class Processes {

    constructor() {
        ipcMain.on('get-processes-data', async (event: any) => {
            event.returnValue = await this.getProcessesData();
        });

        ipcMain.on('get-windows-data', async (event: any, processId: number) => {
            event.returnValue = await this.getWindowData(processId);
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
                     (SELECT start_time, end_time - start_time AS difference FROM heartbeats WHERE IDLE = FALSE) d
                     ON
                         d.start_time = hb.start_time
                         LEFT JOIN
                     processes p on hb.process_id = p.id
                         LEFT JOIN
                     productivity_type pt on p.type_str = pt.type
                WHERE path NOT NULL
                  AND path <> ''
                GROUP BY process_id
                HAVING time > 0
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

    async getWindowData(processId: number) {
        try {
            let results: any = await Database.db.all(`
                SELECT window_id,
                       title,
                       SUM(difference) AS time,
                       CASE
                           WHEN w.type_str IS NULL
                               THEN p.type_str
                           ELSE w.type_str
                           END         AS type,
                       CASE
                           WHEN w.type_str IS NULL
                               THEN pt.color
                           ELSE wt.color
                           END         AS color
                FROM heartbeats AS hb
                         JOIN
                     (SELECT start_time, end_time - start_time AS difference FROM heartbeats WHERE idle = FALSE) d
                     ON d.start_time = hb.start_time
                         LEFT JOIN windows w ON hb.window_id = w.id
                         LEFT JOIN processes p ON p.id = w.process_id
                         LEFT JOIN productivity_type pt on p.type_str = pt.type
                         LEFT JOIN productivity_type wt on w.type_str = wt.type
                WHERE w.process_id = ?
                GROUP BY window_id
                HAVING time > 0
                ORDER BY SUM(difference) DESC`, [processId]);

            return results;
        } catch (e) {
            log.error(e);
        }
    }
}
