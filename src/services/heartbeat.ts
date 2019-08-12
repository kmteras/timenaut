import HeartbeatModel from "../models/heartbeatModel";
import Database from "../models/database";


// WARNING: changing this file does not restart electron properly in development mode
export default class Heartbeat {
    lastHeartbeat?: HeartbeatModel;
    lastEndTime?: number;
    running: boolean;
    timeout: any;

    constructor() {
        this.running = true;
    }

    start() {
        try {
            this.heartbeat(new HeartbeatModel(BigInt(0))).then();
        } catch (e) {
            console.error(e)
        }

        this.timeout = setTimeout(this.start.bind(this), 1000); //TODO: get interval from somewhere
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

        if (this.lastHeartbeat !== undefined) {
            console.log(this.lastHeartbeat);
        }
        console.log(heartbeat);

        if (this.lastHeartbeat !== undefined) {
            if (process.id === this.lastHeartbeat.process.id
                && window.id == this.lastHeartbeat.window.id
                && heartbeat.idle == this.lastHeartbeat.idle) {
                this.lastEndTime = await this.updateHeartbeat(heartbeat, this.lastHeartbeat, this.lastEndTime);
                return;
            }
        }

        this.addHeartbeat(heartbeat, this.lastHeartbeat, this.lastEndTime);
        this.lastHeartbeat = heartbeat;
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

        await Database.db.run(sql, [heartbeat.time, lastHeartbeat.time]);
        return endTime;
    }

    private async addHeartbeat(heartbeat: HeartbeatModel, lastHeartbeat?: HeartbeatModel, lastEndTime?: number) {
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
