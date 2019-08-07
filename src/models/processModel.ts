export default class ProcessModel {
    id?: number;
    path: string;
    name: string;
    type_str?: string;
    type_color?: string;

    constructor(path: string, name: string) {
        this.path = path;
        this.name = name;
    }

    public toString(): string {
        return `ProcessModel: {${this.path}: ${this.name}}`
    }
}
