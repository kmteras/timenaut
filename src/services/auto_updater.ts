import {autoUpdater, UpdateCheckResult} from 'electron-updater';
import log from 'electron-log';

export default class AutoUpdater {
    constructor() {
        autoUpdater.logger = log;
    }

    public check() {
        autoUpdater.checkForUpdatesAndNotify()
            .then((result: UpdateCheckResult | null) => {
                if (result) {
                    log.info(result.versionInfo);
                }
            });
    }
}
