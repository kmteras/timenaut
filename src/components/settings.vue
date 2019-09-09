<template>
    <div id="settings">
        <div class="section">
            <div class="settingsFlex">
                <div class="settingsOption">
                    <label class="checkbox">
                        <input type="checkbox" @change="toggleAutostart(event)" :checked="this.autoStartup">
                        Start on system startup
                    </label>
                </div>
                <span>v{{this.getVersion()}}</span>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import {ipcRenderer} from 'electron';
    import {Updateable} from "@/components/Updateable";

    @Component
    export default class Settings extends Vue implements Updateable {
        autoStartup: boolean = this.hasAutoStart();

        toggleAutostart() {
            this.autoStartup = ipcRenderer.sendSync("autostart-toggle", !this.autoStartup);
        }

        private hasAutoStart(): boolean {
            return ipcRenderer.sendSync("autostart-isenabled");
        }

        update(): void {
        }

        getVersion(): string {
            return ipcRenderer.sendSync('get-version');
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    #settings {
        height: 100%;
    }

    .section {
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 5px 5px 5px grey;
        background-color: white;
        height: 100%;
    }

    .settingsFlex {
        display: flex;
        flex-direction: column;
        text-align: left;
    }

    .settingsOption {
        justify-content: flex-start;
    }
</style>
