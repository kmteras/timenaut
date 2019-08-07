export default class WindowModel {
    id?: number;
    name: string;
    type_str?: string;
    type_color?: string;

    constructor(name: string) {
        this.name = name
    }

    public toString = (): string => {
        return `WindowModel: {${this.name}}`
    }
}
