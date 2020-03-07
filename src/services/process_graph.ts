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
            let results: any = await Database.all(`
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

            let values: Map<string, Map<string, number>> = new Map();

            let types: Map<string, string> = new Map();

            // Group the data
            for (let result of results) {
                types.set(result.type_, result.type_color);

                if (values.has(result.path)) {
                    let typesMap = values.get(result.path)!;
                    typesMap.set(result.type_, result.spent_time);
                    values.set(result.path, typesMap);
                } else {
                    let typesMap = new Map();
                    typesMap.set(result.type_, result.spent_time);
                    values.set(result.path, typesMap);
                }
            }

            let graphValues = Array.from(values);

            graphValues = graphValues.sort((a, b) => {
                const aSum = ProcessGraph.sumIterator(a[1].values());
                const bSum = ProcessGraph.sumIterator(b[1].values());

                if (aSum > bSum) {
                    return -1;
                } else if (bSum > aSum) {
                    return 1;
                } else {
                    return 0;
                }
            });

            // Prepare data for graph
            type Dataset = {
                label: string,
                backgroundColor: string,
                data: number[]
            };

            let datasets: Dataset[] = [];

            // Initialize datasets with eatch type
            for (let [key, value] of types.entries()) {
                datasets.push({
                   label: key,
                   backgroundColor: value,
                   data: []
                });
            }

            // Give datasets the spent type of each type or 0 if the process does not have that type
            let i = 0;
            for (let type of types.keys()) {
                for (let graphValue of graphValues.values()) {
                    let typeTimes = graphValue[1];
                    if (typeTimes.has(type)) {
                        datasets[i].data.push(typeTimes.get(type)!)
                    } else {
                        datasets[i].data.push(0);
                    }
                }
                i++;
            }

            // Sort the datasets
            datasets = datasets.sort((a: Dataset, b: Dataset) => {
                let aSum = a.data.reduce((x, y) => x + y, 0);
                let bSum = b.data.reduce((x, y) => x + y, 0);
                if (aSum > bSum) {
                    return -1;
                } else if (bSum > aSum) {
                    return 1;
                } else {
                    return 0;
                }
            });

            const labels: string[] = [];
            for (let graphValue of graphValues) {
                const label = graphValue[0];

                let regex: RegExp;
                if (process.platform === 'win32') {
                    regex = /\\(.+\\)*(.+)\./;
                } else {
                    regex = /\/(?:,+\/\/)*(.+)\/(.*)/
                }

                if (label.search(regex) < 0) {
                    log.warn(`Could not regex process name from ${label}`);
                    continue;
                }

                let name = label.match(regex)![2];

                labels.push(name);
            }

            return {
                labels: Array.from(labels).slice(0, 8),
                datasets: datasets
            };
        } catch (e) {
            log.error(e);
        }
    }

    private static sumIterator(iterable: IterableIterator<number>): number {
        let sum = 0;
        for (let value of iterable) {
            sum += value;
        }
        return sum;
    }
}
