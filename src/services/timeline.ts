import Database from "@/services/database";
import {ipcMain} from 'electron'
import log from 'electron-log'


export default class Timeline {
    private number: number | null = null;

    constructor() {

    }

    public registerEvents(): void {
        ipcMain.on('get-timeline-data', async (event: any, time: number) => {
            event.returnValue = await this.getData(new Date(time));
        });

        ipcMain.on('get-daily-timeline-data', async (event: any, startTime: number, endTime) => {
            event.returnValue = await this.getDailyData(startTime, endTime);
        });

        ipcMain.on('get-first-date', async (event: any) => {
            event.returnValue = await this.getFirstDate();
        });
    }

    private static valuesSum(values: { [id: string]: number }): number {
        let total = 0;
        for (let key of Object.keys(values)) {
            total += values[key];
        }
        return total;
    }

    async getFirstDate(): Promise<number | null> {
        if (this.number === null) {
            const result = await Database.one(`SELECT MIN(start_time) as start_time FROM heartbeats`);

            this.number = result['start_time'];
        }
        return this.number;
    }

    async getData(date: Date) {
        try {
            let results: any[] = await Database.all(`
                SELECT CASE
                           WHEN w.type_str IS NULL
                               THEN p.type_str
                           ELSE w.type_str
                           END                                                                             AS type_,
                       SUM(hb.end_time - hb.start_time)                                                    AS spent_time,
                       datetime(ROUND(hb.start_time / (60 * 10), 0) * (60 * 10), 'unixepoch', 'localtime') AS timeframe,
                       CASE
                           WHEN w.type_str IS NULL
                               THEN pt.color
                           ELSE wt.color
                           END                                                                             AS type_color
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
                  AND (hb.start_time >= ? OR hb.end_time >= ?)
                  AND (hb.end_time < ? OR hb.start_time < ?)
                GROUP BY ROUND(hb.start_time / (60 * 10), 0) * (60 * 10),
                         type_`, [
                date.getTime() / 1000,
                date.getTime() / 1000,
                date.getTime() / 1000 + 24 * 60 * 60,
                date.getTime() / 1000 + 24 * 60 * 60
            ]);

            let labels = [];
            let values: { [id: string]: number }[] = [];
            let colors: { [id: string]: string } = {};

            for (let h = 0; h < 24; h++) {
                for (let m = 0; m < 60; m += 10) {
                    labels.push(h.toString().padStart(2, "0") + ":" + m.toString().padStart(2, "0"));
                    values.push({});
                }
            }

            let leftoverTime: { [id: string]: number } = {};

            const today = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")}`;

            // If we have time from a heartbeat that started on the previous day, give the time of this day to this day
            for (let value of results) {
                if (value.timeframe.substr(0, 10) !== today.substr(0, 10)) {
                    // Without the 00 time it would be parsed as UTC 00:00
                    const secondsToToday = new Date(today + " 00:00:00").getTime() / 1000 - new Date(value.timeframe).getTime() / 1000;

                    if (value.spent_time - secondsToToday > 0) {
                        results.push({
                            type_: value.type_,
                            spent_time: value.spent_time - secondsToToday,
                            timeframe: today + " 00:00:00",
                            type_color: value.type_color
                        })
                    }
                }
            }

            // TODO: fix all this shit

            for (let h = 0; h < 24; h++) {
                for (let m = 0; m < 60; m += 10) {
                    for (let value of results) {
                        const curHour = h.toString().padStart(2, "0") + ":" + m.toString().padStart(2, "0");
                        if (value.timeframe.substr(0, 16) === today.substr(0, 10) + " " + curHour) {
                            let time: number = value.spent_time;
                            const color: string = value.type_color;
                            const type: string = value.type_;

                            if (type in leftoverTime) {
                                time += leftoverTime[type];
                                leftoverTime[type] = 0;
                            }

                            const totalAlready: number = Timeline.valuesSum(values[h * 6 + m / 10]);
                            time = Math.min(totalAlready + time, 600) - totalAlready;
                            leftoverTime[value.type_] = Math.max(0, value.spent_time - time);

                            values[h * 6 + m / 10][value.type_] = time;
                            colors[value.type_] = color;
                        }
                    }

                    for (let value of Object.keys(leftoverTime)) {
                        if (leftoverTime[value] > 0) {
                            let time = leftoverTime[value];

                            const totalAlready: number = Timeline.valuesSum(values[h * 6 + m / 10]);
                            time = Math.min(totalAlready + time, 600) - totalAlready;
                            leftoverTime[value] = Math.max(0, leftoverTime[value] - time);

                            if (value in values[h * 6 + m / 10]) {
                                values[h * 6 + m / 10][value] += time;
                            } else {
                                values[h * 6 + m / 10][value] = time;
                            }
                        }
                    }
                }
            }

            let datasets = [];

            for (let type of Object.keys(colors)) {
                let data: number[] = [];

                for (let value of values) {
                    if (type in value) {
                        data.push(value[type])
                    } else {
                        data.push(0)
                    }
                }

                datasets.push({
                    label: type,
                    backgroundColor: colors[type],
                    data: data
                });
            }

            return {
                labels: labels,
                datasets: datasets
            }
        } catch (e) {
            log.error(e);
        }
    }

    async getDailyData(startTime: number, endTime: number) {
        try {
            let results: any = await Database.all(`
                SELECT CASE
                           WHEN w.type_str IS NULL
                               THEN p.type_str
                           ELSE w.type_str
                           END                          AS type_,
                       SUM(hb.end_time - hb.start_time) AS spent_time,
                       datetime(
                                   ROUND(
                                           hb.start_time / (60 * 60 * 24), 0) * (60 * 60 * 24), 'unixepoch',
                                   'localtime')         AS date,
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
                GROUP BY ROUND(hb.start_time / (60 * 60 * 24), 0) * (60 * 60 * 24),
                         type_`, [
                startTime / 1000,
                endTime / 1000 + 24 * 60 * 60
            ]);

            let labels: Set<string> = new Set();
            let types: Map<string, string> = new Map();
            let values: Map<string, Map<string, number>> = new Map();

            // TODO: add empty values

            // Group the data
            for (let result of results) {
                let date = result.date.substr(0, 10);
                labels.add(date);
                types.set(result.type_, result.type_color);

                if (values.has(date)) {
                    let typesMap = values.get(date)!;
                    typesMap.set(result.type_, result.spent_time);
                    values.set(date, typesMap);
                } else {
                    let typesMap = new Map();
                    typesMap.set(result.type_, result.spent_time);
                    values.set(date, typesMap);
                }
            }

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
                for (let typeTimes of values.values()) {
                    if (typeTimes.has(type)) {
                        datasets[i].data.push(typeTimes.get(type)!)
                    } else {
                        datasets[i].data.push(0);
                    }
                }
                i++;
            }

            return {
                labels: Array.from(labels),
                datasets: datasets
            }
        } catch (e) {
            log.error(e);
        }
    }
}
