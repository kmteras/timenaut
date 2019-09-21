import activeWin from "active-win";
import ProcessModel from "./processModel";
import WindowModel from "./windowModel";
import {powerMonitor} from "electron"
import Settings from "@/services/settings";


export default class HeartbeatModel {
    // in seconds
    time: number;
    process: ProcessModel;
    window: WindowModel;
    idle: boolean;

    constructor(time: bigint) {
        this.time = Math.floor(new Date().getTime() / 1000);
        const windowInfo = activeWin.sync();

        this.idle = powerMonitor.getSystemIdleTime() > Settings.getIdleTime();

        if (windowInfo !== undefined) {
            this.process = new ProcessModel(windowInfo.owner.path, windowInfo.owner.name);
            this.window = new WindowModel(windowInfo.title, this.process);
        } else {
            throw new Error("Could not get active window");
        }
    }

    public toString(): string {
        return `HeartbeatModel: {${this.time} - idle: ${this.idle}: ${this.process.toString()} ${this.window.toString()}}`
    }
}
