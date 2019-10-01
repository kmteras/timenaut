import Database from "@/services/database";
import {ipcMain} from 'electron'
import log from 'electron-log'


export default class ProcessGraph {
    private number: number | null = null;

    constructor() {
        ipcMain.on('get-process-graph-data', async (event: any, startTime: number, endTime: number) => {
            event.returnValue = await this.getData(startTime, endTime);
        });
    }

    async getData(startTime: number, endTime: number) {
        try {
            let results: any = await Database.db.all(`
                SELECT p.path,
                       CASE
                           WHEN w.type_str IS NULL
                               THEN p.type_str
                           ELSE w.type_str
                           END                          AS type_,
                       SUM(hb.end_time - hb.start_time) AS spent_time,
                       CASE
                           WHEN w.type_str IS NULL
                               THEN pt.color
                           ELSE wt.color
                           END                          AS type_color
                FROM heartbeats AS hb
                         LEFT JOIN
                     windows w ON hb.window_id = w.id
                         LEFT JOIN
                     processes p ON p.id = w.process_id
                         LEFT JOIN
                     productivity_type pt on p.type_str = pt.type
                         LEFT JOIN
                     productivity_type wt on w.type_str = wt.type
                WHERE hb.idle = FALSE
                  AND hb.start_time > ?
                  AND hb.end_time < ?
                GROUP BY type_, p.path
                ORDER BY spent_time DESC`, [
                startTime / 1000,
                endTime / 1000 + 24 * 60 * 60
            ]);

            log.debug(results);

            let labels: Set<string> = new Set();
            let values: Map<string, { type: string, time: number }[]> = new Map();

            // Group the data
            for (let result of results) {
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

                let name = result.path.match(regex)[2];

                labels.add(name);

                if (values.has(result.path)) {
                    let processValues = values.get(result.path);
                    processValues!.push({type: result.type_, time: result.spent_time});
                    values.set(result.path, processValues!);
                } else {
                    values.set(result.path, [{
                        type: result.type_,
                        time: result.spent_time
                    }]);
                }
            }

            // Prepare data for graph
            type Dataset = {
                label: string,
                backgroundColor: string,
                data: number[]
            };

            console.log(values);

            let datasets: Dataset[] = [];

            return {
                labels: Array.from(labels),
                datasets: Array.from(datasets.values())
            };
        } catch (e) {
            log.error(e);
        }
    }
}
