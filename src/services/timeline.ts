import Database from "@/models/database";
import {ipcMain} from 'electron'


export default class Timeline {
    db: Database;

    constructor(db: Database) {
        this.db = db;
        ipcMain.on('get-timeline-data', async (event: any, arg: any) => {
            event.returnValue = await this.getData();
        })
    }

    async getData() {
        try {
            let results = await this.db.all(`
SELECT
    CASE
        WHEN w.type_str IS NULL
            THEN p.type_str
        ELSE w.type_str
    END AS type_,
    SUM(hb.end_time - hb.start_time) AS spent_time,
    datetime(ROUND(hb.start_time / (60 * 10), 0) * (60 * 10), 'unixepoch', 'localtime') AS timeframe,
    CASE
        WHEN w.type_str IS NULL
            THEN pt.color
        ELSE wt.color
    END AS type_color
FROM
    heartbeats AS hb
LEFT JOIN
    windows w ON hb.window_id = w.id
LEFT JOIN
    processes p ON p.id = w.process_id
LEFT JOIN
    productivity_type pt on p.type_str = pt.type
LEFT JOIN
    productivity_type wt on w.type_str = wt.type
WHERE
    hb.idle = FALSE
GROUP BY
    ROUND(hb.start_time / (60 * 10), 0) * (60 * 10),
    type_`);

            let labels = [];

            for (let h = 0; h < 24; h++) {
                for (let m = 0; m < 60; m += 10) {
                    labels.push(h.toString().padStart(2, "0") + ":" + m.toString().padStart(2, "0"));
                }
            }

            let leftoverTime = {};

            for (let h = 0; h < 24; h++) {
                for (let m = 0; m < 60; m += 10) {
                    labels.push(h.toString().padStart(2, "0") + ":" + m.toString().padStart(2, "0"));
                }
            }

            // console.log(results);
            return {
                labels: labels,
                datasets: [
                    {
                        label: 'Work',
                        backgroundColor: '#f87979',
                        data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
                    },
                    {
                        label: 'School',
                        backgroundColor: '#f879f8',
                        data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
                    }
                ]
            }
        } catch (e) {
            console.error(e);
        }
    }
}
