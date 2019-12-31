import activeWin from "active-win";
import ProcessModel from "@/models/process_model";
import WindowModel from "@/models/window_model";
import {powerMonitor} from "electron"
import Settings from "@/services/settings";
import getActiveWindow from "@/util/active_window_linux";


export default class HeartbeatModel {
    // in seconds
    time: number;
    process: ProcessModel;
    window: WindowModel;
    idle: boolean;

    constructor() {
        this.time = Math.floor(new Date().getTime() / 1000);
        const windowInfo = activeWin.sync();

        this.idle = powerMonitor.getSystemIdleTime() > Settings.getIdleTime();

        if (windowInfo !== undefined) {
            this.process = new ProcessModel(windowInfo.owner.path, windowInfo.owner.name);
            this.window = new WindowModel(windowInfo.title, this.process);
        } else {
            /**
             * On Linux some X11 windows do not have a PID attached to them. (Process created with another process?)
             * Module active-win fails on that.
             * We can still get the active window but it will associated with a process.
             */

            if (process.platform === 'linux') {
                try {
                    const windowName = getActiveWindow();
                    this.process = new ProcessModel("/unknown/unknown", "unknown");
                    this.window = new WindowModel(windowName, this.process);
                } catch (_) {
                    throw new Error("Could not get a active window");
                }
            } else {
                throw new Error("Could not get active window");
            }
        }
    }

    public toString(): string {
        return `HeartbeatModel: {${this.time} - idle: ${this.idle}: ${this.process.toString()} ${this.window.toString()}}`
    }
}
