import activeWin from "active-win";
import ProcessModel from "./processModel";
import WindowModel from "./windowModel";

export default class HeartbeatModel {
    time: number;
    process: ProcessModel;
    window: WindowModel;

    constructor(time: bigint) {
        this.time = Math.floor(new Date().getTime() / 1000);
        const windowInfo = activeWin.sync();

        if (windowInfo !== undefined) {
            this.process = new ProcessModel(windowInfo.owner.path, windowInfo.owner.name);
            this.window = new WindowModel(windowInfo.title, this.process);
        } else {
            throw new Error("Could not get active window");
        }
    }

    public toString(): string {
        return `HeartbeatModel: {${this.time}: ${this.process.toString()} ${this.window.toString()}}`
    }
}
