import Database from "../models/database";
import {ipcMain} from 'electron'


export default class DailyPieChart {
    constructor() {
        ipcMain.on('get-pie-data', async (event: any, arg: any) => {
            event.returnValue = await this.getData();
        })
    }

    async getData() {
        try {
            let results: any = await Database.db.all(`
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
                Date.now() / 1000 - 500000, // TODO: fix time
                Date.now()
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
            console.error(e);
        }
    }
}
