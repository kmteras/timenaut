import ProcessModel from "./processModel";
import WindowModel from "./windowModel";

export default class HeartbeatModel {
    time: bigint;
    process?: ProcessModel;
    window?: WindowModel;

    constructor(time: bigint) {
        this.time = time
    }
}
