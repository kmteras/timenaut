import HeartbeatModel from "../models/heartbeatModel";
import Database from "../models/database";
import ProcessModel from "@/models/processModel";

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
            await heartbeat.process.save();
        }

        let window = await heartbeat.window.find();

        if (window == null) {
            await heartbeat.window.save();
        }
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
