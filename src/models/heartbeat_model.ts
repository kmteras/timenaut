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

    constructor(time: number, process: ProcessModel, window: WindowModel, idle: boolean) {
        this.time = time;
        this.process = process;
        this.window = window;
        this.idle = idle;
    }

    static getCurrentHeartbeat(): HeartbeatModel {
        const time = Math.floor(new Date().getTime() / 1000);
        const windowInfo = activeWin.sync();

        const idle = powerMonitor.getSystemIdleTime() > Settings.getIdleTime();

        let processModel;
        let windowModel;

        if (windowInfo !== undefined) {
            processModel = new ProcessModel(windowInfo.owner.path, windowInfo.owner.name);
            windowModel = new WindowModel(windowInfo.title, processModel);
        } else {
            /**
             * On Linux some X11 windows do not have a PID attached to them. (Process created with another process?)
             * Module active-win fails on that.
             * We can still get the active window but it will associated with a process.
             */

            if (process.platform === 'linux') {
                try {
                    const windowName = getActiveWindow();
                    processModel = new ProcessModel("/unknown/unknown", "unknown");
                    windowModel = new WindowModel(windowName, processModel);
                } catch (_) {
                    throw new Error("Could not get a active window");
                }
            } else {
                throw new Error("Could not get active window");
            }
        }
        return new HeartbeatModel(time, processModel, windowModel, idle);
    }

    public toString(): string {
        return `HeartbeatModel: {${this.time} - idle: ${this.idle}: ${this.process.toString()} ${this.window.toString()}}`
    }
}
