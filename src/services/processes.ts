import Database from "@/services/database";
import {ipcMain} from 'electron'
import log from 'electron-log'
import {getDayLength} from "@/util/timeUtil";


export default class Processes {

    constructor() {
        ipcMain.on('get-processes-data', async (event: Event, startTime: number, endTime: number) => {
            event.returnValue = await this.getProcessesData(startTime, endTime);
        });

        ipcMain.on('get-windows-data', async (event: Event, startTime: number, endTime: number, processId: number) => {
            event.returnValue = await this.getWindowData(startTime, endTime, processId);
        });

        ipcMain.on('get-type-data', async (event: Event) => {
            event.returnValue = await this.getTypeData();
        });

        ipcMain.on('set-process-type', async (event: Event, processId: number, type: string) => {
            await this.setProcessType(processId, type);
            event.returnValue = true;
        });

        ipcMain.on('set-window-type', async (event: Event, windowId: number, type: string) => {
            await this.setWindowType(windowId, type);
            event.returnValue = true;
        });
    }

    async getProcessesData(startTime: number, endTime: number) {
        try {
            let results: any = await Database.db.all(`
                SELECT path,
                       SUM(difference) AS time,
                       process_id      as id,
                       pt.type,
                       pt.color
                FROM heartbeats AS hb
                         JOIN
                     (SELECT start_time, end_time - start_time AS difference
                      FROM heartbeats hb
                      WHERE hb.IDLE = FALSE
                        AND hb.start_time > ?
                        AND hb.end_time < ?) d
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
                ORDER BY SUM(difference) DESC`, [startTime / 1000, endTime / 1000 + getDayLength()]);

            for (let result of results) {
                if (result.name == undefined) {
                    let regex: RegExp;
                    if (process.platform === 'win32') {
                        regex = /\\(.+\\)*(.+)\./;
                    } else {
                        regex = /\/(?:,+\/\/)*(.+)\/(.*)/
                    }

                    if (result.path.search(regex) < 0) {
                        log.warn(`Could not regex process name from ${result.path}`);
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

    async getWindowData(startTime: number, endTime: number, processId: number) {
        try {
            let results: any = await Database.db.all(`
                SELECT window_id       as id,
                       w.title,
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
                     (SELECT start_time, end_time - start_time AS difference
                      FROM heartbeats hb
                      WHERE hb.idle = FALSE
                        AND hb.start_time > ?
                        AND hb.end_time < ?) d
                     ON d.start_time = hb.start_time
                         LEFT JOIN windows w ON hb.window_id = w.id
                         LEFT JOIN processes p ON p.id = w.process_id
                         LEFT JOIN productivity_type pt on p.type_str = pt.type
                         LEFT JOIN productivity_type wt on w.type_str = wt.type
                WHERE w.process_id = ?
                GROUP BY window_id
                HAVING time > 0
                ORDER BY SUM(difference) DESC`, [startTime / 1000, endTime / 1000 + getDayLength(), processId]);

            return results;
        } catch (e) {
            log.error(e);
        }
    }

    async getTypeData() {
        try {
            let results: any = await Database.db.all(`
                SELECT type,
                       color
                FROM productivity_type
                WHERE type != 'unknown'`);

            return results;
        } catch (e) {
            log.error(e);
        }
    }

    async setProcessType(processId: number, type: string) {
        try {
            await Database.db.run(`
                UPDATE processes
                SET type_str=?
                WHERE id = ?
            `, [type, processId]);
        } catch (e) {
            log.error(e);
        }
    }

    async setWindowType(windowId: number, type: string) {
        try {
            await Database.db.run(`
                UPDATE windows
                SET type_str=?
                WHERE id = ?
            `, [type, windowId]);
        } catch (e) {
            log.error(e);
        }
    }
}
