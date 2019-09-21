import HeartbeatModel from "../models/heartbeatModel";
import Database from "../models/database";
import log from 'electron-log'
import BrowserWindow = Electron.BrowserWindow;


// WARNING: changing this file does not restart electron properly in development mode
export default class Heartbeat {
    private lastHeartbeat: HeartbeatModel | null = null;
    private lastEndTime: number | null = null;
    running: boolean;
    private paused: boolean;
    private timeout: any;
    private win: BrowserWindow;
    private pollTime: number = 1;
    private pauseTimeout: any = null;

    constructor(window: BrowserWindow) {
        this.running = true;
        this.paused = false;
        this.win = window;
    }

    start() {
        try {
            this.heartbeat(new HeartbeatModel(BigInt(0))).then();
        } catch (e) {
            // Tough shit, cant really do anything - not a severe problem
            log.debug(e)
        }

        if (this.running) {
            this.timeout = setTimeout(this.start.bind(this), this.pollTime * 1000); //TODO: get interval from somewhere
        }
    }

    private async heartbeat(heartbeat: HeartbeatModel) {
        if (this.paused) {
            return;
        }

        let process = await heartbeat.process.find();

        if (process == null) {
            process = await heartbeat.process.save();
        }

        let window = await heartbeat.window.find();

        if (window == null) {
            window = await heartbeat.window.save();
        }

        log.debug(heartbeat.toString());

        if (this.lastHeartbeat !== null) {
            if (process.id === this.lastHeartbeat.process.id
                && window.id == this.lastHeartbeat.window.id
                && heartbeat.idle == this.lastHeartbeat.idle) {
                this.lastEndTime = await this.updateHeartbeat(heartbeat, this.lastHeartbeat, this.lastEndTime);
                this.win.webContents.send('heartbeat');
                return;
            }
        }

        this.addHeartbeat(heartbeat, this.lastHeartbeat);
        this.lastEndTime = heartbeat.time;
        this.lastHeartbeat = heartbeat;
        this.win.webContents.send('heartbeat');
    }

    private async updateHeartbeat(heartbeat: HeartbeatModel,
                                  lastHeartbeat: HeartbeatModel, lastEndTime: number | null): Promise<number> {
        const sql = `
            UPDATE heartbeats
            SET end_time=?
            WHERE start_time = ?
        `;

        let endTime = heartbeat.time;

        if (lastEndTime !== null) {
            // TODO: get poll time from settings
            let possibleEndTime = lastEndTime + this.pollTime;
            if (heartbeat.time > possibleEndTime) {
                endTime = possibleEndTime;

                // Reset the last heartbeat and start again
                this.lastHeartbeat = null;
            }
        }

        await Database.db.run(sql, [endTime, lastHeartbeat.time]);
        return endTime;
    }

    private async addHeartbeat(heartbeat: HeartbeatModel, lastHeartbeat: HeartbeatModel | null) {
        if (lastHeartbeat !== null) {
            await this.updateHeartbeat(heartbeat, lastHeartbeat, this.lastEndTime)
        }

        const sql = `
            INSERT INTO heartbeats (process_id, window_id, start_time, end_time, idle)
            VALUES (?, ?, ?, ?, ?)
        `;
        await Database.db.run(sql,
            [heartbeat.process.id, heartbeat.window.id, heartbeat.time, heartbeat.time, heartbeat.idle])
    }

    public pause(time: number | null, resumeCallback: () => void) {
        log.info(`Paused tracking for ${time} seconds`);
        this.paused = true;
        if (time !== null) {
            this.pauseTimeout = setTimeout(() => {
                this.resume(resumeCallback)
            }, time * 1000);
        }
    }

    public resume(resumeCallback: () => void) {
        if (this.pauseTimeout != null) {
            clearTimeout(this.pauseTimeout)
        }
        this.paused = false;
        resumeCallback();
    }
}
