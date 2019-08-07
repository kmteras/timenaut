import HeartbeatModel from "../models/heartbeatModel";
import Database from "../models/database";

// WARNING: changing this file does not restart electron properly in development mode
export default class Heartbeat {
    lastProcessId = null;
    lastWindowId = null;
    lastStartTime = null;
    lastEndTime = null;
    lastIdle: boolean = false;
    running: boolean;
    timeout: any;

    constructor() {
        this.running = true;
    }

    start() {
        this.timeout = setTimeout(this.heartbeat.bind(this), 1000); //TODO: get interval from somewhere
    }

    heartbeat() {
        try {
            let heartbeat = new HeartbeatModel(BigInt(0));
            console.log(heartbeat.toString());
        } catch (e) {
            console.error(e)
        }
        this.timeout = setTimeout(this.heartbeat.bind(this), 1000); //TODO: get interval from somewhere
    }

    private async updateHeartbeat() {
        const sql = `
            UPDATE heartbeats
            SET end_time=?
            WHERE start_time = ?
        `;

        await Database.db.run(sql, [])
    }

    private async addHeartbeat() {
        const sql = `
            INSERT INTO heartbeats (process_id, window_id, start_time, end_time, idle)
            VALUES (?, ?, ?, ?, ?)
        `;
        await Database.db.run(sql, [])
    }
}
