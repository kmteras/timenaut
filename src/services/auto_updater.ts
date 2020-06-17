import {autoUpdater, UpdateCheckResult} from 'electron-updater';
import log from 'electron-log';
import notifier from 'node-notifier'

export default class AutoUpdater {
    private iconUrl?: string;

    constructor() {
        autoUpdater.logger = log;
    }

    public check() {
        this.displayNotification('Checking for updates');

        autoUpdater.checkForUpdatesAndNotify()
            .then((result: UpdateCheckResult | null) => {
                if (result) {
                    log.info(result.updateInfo);
                    this.displayNotification('Checking for updates finished');
                } else {
                    this.displayNotification('No update available');
                }
            })
            .catch((e) => {
                this.displayNotification('Error occurred while checking for updates');
                log.error("Error checking for updates", e);
            });
    }

    public setIconUrl(url: string) {
        this.iconUrl = url;
    }

    private displayNotification(text: string) {
        notifier.notify({
            title: 'Timenaut',
            icon: this.iconUrl,
            message: text
        });
    }
}
