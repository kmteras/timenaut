import Database from "@/services/database";
import {ipcMain} from 'electron'
import log from "electron-log";


export default class DailyPieChart {
    constructor() {
        ipcMain.on('get-pie-data', async (event: any, startTime: number, endTime) => {
            event.returnValue = await this.getData(startTime, endTime);
        })
    }

    async getData(startTime: number, endTime: number) {
        try {
            let results: any = await Database.all(`
                SELECT SUM(difference) as total_time,
                       CASE
                           WHEN w.type_str IS NULL
                               THEN p.type_str
                           ELSE w.type_str
                           END AS _type,
                       CASE
                           WHEN w.type_str IS NULL
                               THEN pt.color
                           ELSE wt.color
                           END AS type_color
                FROM heartbeats AS hb
                         JOIN
                     (SELECT start_time,
                             end_time - start_time AS difference
                      FROM heartbeats) d
                     ON
                         d.start_time = hb.start_time
                         LEFT JOIN windows w ON hb.window_id = w.id
                         LEFT JOIN processes p ON p.id = w.process_id
                         LEFT JOIN productivity_type pt on p.type_str = pt.type
                         LEFT JOIN productivity_type wt on w.type_str = wt.type
                WHERE d.start_time > ?
                  AND d.start_time < ?
                  AND hb.idle = FALSE
                GROUP BY _type
                ORDER BY SUM(difference) DESC
            `, [
                startTime / 1000,
                endTime / 1000 + 24 * 60 * 60
            ]);

            return {
                labels: results.map((v: any) => {return v._type}),
                datasets: [
                    {
                        label: "Test",
                        backgroundColor: results.map((v: any) => {return v.type_color}),
                        data: results.map((v: any) => {return v.total_time})
                    }
                ]
            };
        } catch (e) {
            log.error(e);
        }
    }
}
