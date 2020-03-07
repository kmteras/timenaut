import WindowModel from "@/models/window_model";
import Database from "@/services/database";
import log from 'electron-log';

export default class DatabaseConversionService {

    private static SPLIT_CHARACTERS = ["-", "|", "·"];

    public async convert() {
        log.debug("Starting convertsion");
        let windows = await this.queryAllWindows();
        this.splitWindowNames(windows);
    }

    public splitWindowNames(windows: WindowModel[]): string[][] {
        let splitWindowTitles: string[][] = [];
        for (let window of windows) {
            splitWindowTitles.push(this.splitWindowName(window.title));
        }
        return splitWindowTitles;
    }

    public splitWindowName(title: string): string[] {
        let splits = [title];

        for (let splitChar of DatabaseConversionService.SPLIT_CHARACTERS) {
            for (const [index, split] of splits.entries()) {
                const splitResult = split.split(` ${splitChar} `);

                if (splitResult.length > 1) {
                    splits[index] = splitResult[0];

                    for (let i = 1; i < splitResult.length; i ++) {
                        splits.splice(index + i, 0, splitResult[i])
                    }
                }
            }
        }

        log.debug(splits, title);

        return splits;
    }

    private async queryAllWindows(): Promise<WindowModel[]> {
        return await Database.all("SELECT * FROM windows") as WindowModel[];
    }
}
