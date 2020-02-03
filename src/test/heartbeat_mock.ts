import ProcessModel from "@/models/process_model";
import WindowModel from "@/models/window_model";
import Database from "@/services/database";

export default class HeartbeatMock {
    public async mock(startTime: number, endTime: number, process: string, window: string) {
        let processModel = new ProcessModel(process, process);
        let windowModel = new WindowModel(window, processModel);

        processModel = await processModel.save();
        windowModel = await windowModel.save();

        await Database.db.run(`
            INSERT INTO heartbeats(process_id, window_id, start_time, end_time, idle)
            VALUES (?, ?, ?, ?, ?)
        `, [processModel.id, windowModel.id, startTime / 1000, endTime / 1000, false])
    }

    public async mockLength(startTime: number, length: number, process: string, window: string) {
        await this.mock(startTime, startTime + length * 1000, process, window);
    }
}
