import ProcessModel from './processModel'

export default class WindowModel {
    id?: number;
    name: string;
    type_str?: string;
    type_color?: string;
    process?: ProcessModel;

    constructor(name: string) {
        this.name = name
    }
}
