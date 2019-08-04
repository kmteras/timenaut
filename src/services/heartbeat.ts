import activeWin from "active-win";
import HeartbeatModel from "../models/heartbeatModel";
import Database from "../models/database";


export default class Heartbeat {
    lastProcessId = null;
    lastWindowId = null;
    lastStartTime = null;
    lastEndTime = null;
    lastIdle: boolean = false;
    db: Database;

    constructor(db: Database) {
        this.db = db;
    }

    start() {
        // console.log(activeWin.sync());
        this.heartbeat(new HeartbeatModel(BigInt(0)));
        setTimeout(this.start.bind(this), 1000);
    }

    heartbeat(heartbeat: HeartbeatModel) {

    }

    private async updateHeartbeat() {
        const sql = `
            UPDATE heartbeats
            SET end_time=?
            WHERE start_time = ?
        `;

        await this.db.run(sql, [])
    }

    private async addHeartbeat() {
        const sql = `
            INSERT INTO heartbeats (process_id, window_id, start_time, end_time, idle)
            VALUES (?, ?, ?, ?, ?)
        `;
        await this.db.run(sql, [])
    }
}
