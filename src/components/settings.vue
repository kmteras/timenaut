<template>
    <div id="settings">
        <div class="section">
            <div class="settingsFlexRow">
                <h3 class="settingsTitle">Settings</h3>
                <hr id="settingsHr">
                <div class="settingsFlexColumn" id="main1">
                    <div class="settingsOption">
                        <label>
                            <p>Start on system startup <input type="checkbox" @change="toggleAutostart" :checked="this.autoStartup"></p>


                        </label>
                    </div>
                    <div class="settingsOption">
                        <label>
                            Poll time in seconds
                            <input type="number" min="1" max="300" @change="changePollTime"
                                   :value="this.getSetting('heartbeatPollTime')">
                        </label>
                    </div>
                    <div class="settingsOption">
                        <label>
                            Idle time in seconds
                            <input type="number" min="10" max="3600" @change="changeIdleTime"
                                   :value="this.getSetting('heartbeatIdleTime')">
                        </label>
                    </div>
                    <div class="settingsOption" v-if="isDevelopment">
                        <button @click="convert">Convert</button>
                    </div>

                </div>
                <div class="settingsFlexColumn" id="main2">
                </div>
                <p class="settingsLink">Found a bug? <a @click="openGitHub">Let us know!</a></p>
                <span class="settingsVersion">v{{this.getVersion()}}</span>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import ipcRenderer from '@/components/ipc_renderer';
    import Updatable from "@/components/updatable";
    import {shell} from 'electron';

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
            this.setSetting('heartbeatIdleTime', event.target.value);
        }

        private hasAutoStart(): boolean {
            return ipcRenderer.sendSync("autostart-isenabled");
        }

        update(): void {
        }

        protected isDevelopment(): boolean {
            return ipcRenderer.sendSync('is-development');
        }

        protected getVersion(): string {
            return ipcRenderer.sendSync('get-version');
        }

        protected getSetting(key: string): string {
            return ipcRenderer.sendSync('get-setting', key);
        }

        protected convert(): void {
            ipcRenderer.send('convert');
        }

        protected setSetting(key: string, value: string) {
            return ipcRenderer.sendSync('set-setting', key, value);
        }

        public openGitHub() {
            shell.openExternal("https://github.com/kmteras/timenaut/issues")
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

    .settingsFlexColumn {
        display: flex;
        flex-direction: column;
        text-align: left;
        height: 100%;
        margin: 15px;
    }

    .settingsFlexRow {
        display: grid;
        grid-template-columns: 50% 50%;
        grid-template-rows: 10% 86% 4%;
        height: 100%;
        grid-template-areas:
                "header header"
                "main1 main2"
                "footer footer";
    }

    #main1 {
        grid-area: main1;
        flex-grow: 1;
    }
    #main2 {
        grid-area: main2;
        flex-grow: 1;
    }

    #settingsHr{
        width: 80%;
        grid-area: header;
        text-align: center;
        align-items: center;
        margin: 2rem 0 0 10% !important;
        height: 1px;
        background: -webkit-gradient(radial, 50% 50%, 0, 50% 50%, 350, from(gray), to(#fff));
    }

    .settingsTitle {
        text-align: center;
        grid-area: header;
    }

    .settingsLink {
        text-align: left;
        grid-area: footer;
    }

    .settingsOption {
        justify-content: flex-start;
        margin-bottom: 10px;
    }

    .settingsVersion {
        text-align: right;
        color: #476582;
        grid-area: footer;

    }
</style>
