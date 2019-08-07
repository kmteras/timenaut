import Database from "./database";
import ProcessModel from "./processModel";

export default class WindowModel {
    id?: number;
    title: string;
    type_str?: string;
    type_color?: string;
    process: ProcessModel;

    constructor(title: string, process: ProcessModel) {
        this.title = title;
        this.process = process;
    }

    async save() {
        await Database.db.run(`
            INSERT INTO windows (process_id, title)
            VALUES (?, ?)`, [this.process.id, this.title])
    }

    async find(): Promise<WindowModel | null> {
        let response = await Database.db.one(`
            SELECT *
            FROM windows
            WHERE title = ?
        `, [this.title]) as WindowModel;

        if (response !== undefined) {
            this.id = response.id;
            this.type_str = response.type_str;
            return this;
        } else {
            return null;
        }
    }

    public toString = (): string => {
        return `WindowModel: {${this.title}}`
    }
}
