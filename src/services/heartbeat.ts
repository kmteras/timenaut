import HeartbeatModel from "../models/heartbeatModel";
import Database from "../models/database";
import log from 'electron-log'
import BrowserWindow = Electron.BrowserWindow;


// WARNING: changing this file does not restart electron properly in development mode
export default class Heartbeat {
    lastHeartbeat?: HeartbeatModel;
    lastEndTime?: number;
    running: boolean;
    timeout: any;
    private win: BrowserWindow;

    constructor(window: BrowserWindow) {
        this.running = true;
        this.win = window;
    }

    start() {
        try {
            this.heartbeat(new HeartbeatModel(BigInt(0))).then();
        } catch (e) {
            // Tough shit, cant really do anything - not a severe problem
            log.warn(e)
        }

         if (this.running) {
             this.timeout = setTimeout(this.start.bind(this), 1000); //TODO: get interval from somewhere
         }
    }

    async heartbeat(heartbeat: HeartbeatModel) {
        let process = await heartbeat.process.find();

        if (process == null) {
            process = await heartbeat.process.save();
        }

        let window = await heartbeat.window.find();

        if (window == null) {
            window = await heartbeat.window.save();
        }

        log.debug(heartbeat.toString());

        if (this.lastHeartbeat !== undefined) {
            if (process.id === this.lastHeartbeat.process.id
                && window.id == this.lastHeartbeat.window.id
                && heartbeat.idle == this.lastHeartbeat.idle) {
                this.lastEndTime = await this.updateHeartbeat(heartbeat, this.lastHeartbeat, this.lastEndTime);
                this.win.webContents.send('heartbeat');
                return;
            }
        }

        this.addHeartbeat(heartbeat, this.lastHeartbeat);
        this.lastHeartbeat = heartbeat;
        this.win.webContents.send('heartbeat');
    }

    private async updateHeartbeat(heartbeat: HeartbeatModel,
                                  lastHeartbeat: HeartbeatModel, lastEndTime?: number): Promise<number> {
        const sql = `
            UPDATE heartbeats
            SET end_time=?
            WHERE start_time = ?
        `;

        let endTime = heartbeat.time;

        if (lastEndTime !== undefined) {
            endTime = Math.min(heartbeat.time, lastEndTime + 1000); // TODO: get poll time from settings
        }

        await Database.db.run(sql, [endTime, lastHeartbeat.time]);
        return endTime;
    }

    private async addHeartbeat(heartbeat: HeartbeatModel, lastHeartbeat?: HeartbeatModel) {
        if (lastHeartbeat !== undefined) {
            await this.updateHeartbeat(heartbeat, lastHeartbeat)
        }

        const sql = `
            INSERT INTO heartbeats (process_id, window_id, start_time, end_time, idle)
            VALUES (?, ?, ?, ?, ?)
        `;
        await Database.db.run(sql,
            [heartbeat.process.id, heartbeat.window.id, heartbeat.time, heartbeat.time, heartbeat.idle])
    }
}
