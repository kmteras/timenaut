import Database from "@/services/database";


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

    async save(): Promise<ProcessModel> {
        await Database.run(`
            INSERT INTO processes (path, type_str)
            VALUES (?, 'unknown')`, [this.path]);

        let newProcess = await this.find();

        if (newProcess === undefined) {
            throw Error("Could not find just saved process");
        }

        return newProcess;
    }

    async find(): Promise<ProcessModel | undefined> {
        let response = await Database.one(`
            SELECT *
            FROM processes
            WHERE path = ?
        `, [this.path]) as ProcessModel;

        if (response !== undefined) {
            this.id = response.id;
            this.type_str = response.type_str;
            return this;
        } else {
            return undefined;
        }
    }

    public toString(): string {
        return `ProcessModel: {${this.path}: ${this.name}}`
    }
}
