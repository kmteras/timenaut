<template>
    <div id="settings">
        <div class="section">
            <div class="settingsFlex">
                <div class="settingsOption">
                    <label>
                        <input type="checkbox" @change="toggleAutostart" :checked="this.autoStartup">
                        Start on system startup
                    </label>
                </div>
                <div class="settingsOption">
                    <label>
                        <input type="number" min="1" max="300" @change="changePollTime"
                               :value="this.getSetting('heartbeatPollTime')">
                        Poll time in seconds
                    </label>
                </div>
                <div class="settingsOption">
                    <label>
                        <input type="number" min="10" max="3600" @change="changeIdleTime"
                               :value="this.getSetting('heartbeatIdleTime')">
                        Idle time in seconds
                    </label>
                </div>
                <span class="settingsFill"></span>
                <span class="settingsVersion">v{{this.getVersion()}}</span>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import ipcRenderer from '@/components/ipcRenderer';
    import Updatable from "@/components/updatable";

    @Component
    export default class Settings extends Vue implements Updatable {
        autoStartup: boolean = this.hasAutoStart();

        protected toggleAutostart() {
            this.autoStartup = ipcRenderer.sendSync("autostart-toggle", !this.autoStartup);
        }

        protected changePollTime(event: any) {
            this.setSetting('heartbeatPollTime', event.target.value);
        }

        protected changeIdleTime(event: any) {
            this.setSetting('changeIdleTime', event.target.value);
        }

        private hasAutoStart(): boolean {
            return ipcRenderer.sendSync("autostart-isenabled");
        }

        update(): void {
        }

        protected getVersion(): string {
            return ipcRenderer.sendSync('get-version');
        }

        protected getSetting(key: string): string {
            return ipcRenderer.sendSync('get-setting', key);
        }

        protected setSetting(key: string, value: string) {
            return ipcRenderer.sendSync('set-setting', key, value);
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    #settings {
        display: grid;
        height: 100%;
    }

    .section {
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 5px 5px 5px grey;
        background-color: white;
    }

    .settingsFlex {
        display: flex;
        flex-direction: column;
        text-align: left;
        height: 100%;
    }

    .settingsFill {
        flex-grow: 1;
    }

    .settingsOption {
        justify-content: flex-start;
        margin-bottom: 10px;
    }

    .settingsVersion {
        text-align: right;
    }
</style>
