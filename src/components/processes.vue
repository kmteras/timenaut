<template>
    <div id="processes">
        <div class="section" id="infoSection">
            <div v-if="selectedWindow !== null">
                <p>{{"Window: " + selectedWindow.title}}</p>
            </div>
            <div v-else-if="selectedProcess !== null">
                <p>{{"Path: " + selectedProcess.path}}</p>
            </div>

            <div v-if="selectedWindow !== null">
                <p>{{"Process: " + selectedProcess.name}}</p>
            </div>
            <div v-else-if="selectedProcess !== null">
                <p>{{"Process: " + selectedProcess.name}}</p>
            </div>

            <div v-if="selectedWindow !== null">
                <p>{{"Time: " + timeAsString(selectedWindow.time)}}</p>
            </div>
            <div v-else-if="selectedProcess !== null">
                <p>{{"Time: " + timeAsString(selectedProcess.time)}}</p>
            </div>

            <div v-if="selectedWindow !== null">
                <label for="windowTypeSelection">Type</label>
                <select id="windowTypeSelection" :style="{color: selectedWindow.color}" @change="setWindowType">
                    <option :value="selectedWindow.type" :style="{color: selectedWindow.color}">
                        {{selectedWindow.type}}
                    </option>
                    <option v-for="(typeData, idx) in this.getTypesBesides(selectedWindow.type)"
                            :key="idx" :value="typeData.type"
                            :style="{color: typeData.color}">
                        {{typeData.type}}
                    </option>
                </select>
            </div>
            <div v-else-if="selectedProcess !== null">
                <label for="processTypeSelection">Type</label>
                <select id="processTypeSelection" :style="{color: selectedProcess.color}" @change="setProcessType">
                    <option :value="selectedProcess.type" :style="{color: selectedProcess.color}">
                        {{selectedProcess.type}}
                    </option>
                    <option v-for="(typeData, idx) in this.getTypesBesides(selectedProcess.type)"
                            :key="idx" :value="typeData.type"
                            :style="{color: typeData.color}">
                        {{typeData.type}}
                    </option>
                </select>
            </div>
        </div>
        <div class="section" id="tableSection">
            <div id="processTableSection">
                <table class="table is-narrow" id="processTable">
                    <thead>
                    <tr>
                        <th>Process</th>
                        <th class="timeHeader">Time</th>
                    </tr>
                    </thead>
                    <tbody v-for="(process, idx) in this.processData" :key="idx" @click="clickProcess(process)">
                    <tr class='hover' :class="{selected: selectedProcessId === process.process_id}">
                        <td :style="{color: process.color}">{{process.name}}</td>
                        <td>{{timeAsString(process.time)}}</td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div id="windowTableSection">
                <table class="table is-narrow" id="windowTable">
                    <thead>
                    <tr>
                        <th>Window</th>
                        <th class="timeHeader">Time</th>
                    </tr>
                    </thead>
                    <tbody v-for="(window, idx) in this.windowData" :key="idx" @click="clickWindow(window)">
                    <tr class='hover' :class="{selected: selectedWindowId === window.window_id}">
                        <td :style="{color: window.color}">{{window.title}}</td>
                        <td>{{timeAsString(window.time)}}</td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Provide, Vue} from 'vue-property-decorator';
    import {ipcRenderer} from 'electron';
    import ContentPage from "@/components/contentPage.vue";
    import {Updateable} from "@/components/Updateable";

    declare interface ProcessData {
        path: string,
        name: string,
        time: number,
        process_id: number,
        type: string,
        color: string
    }

    declare interface WindowData {
        title: string,
        time: number,
        window_id: number,
        type: string,
        color: string
    }

    declare interface TypeData {
        type: string,
        color: string
    }

    @Component
    export default class Processes extends Vue implements ContentPage, Updateable {
        @Provide() message = 'message';
        selectedProcess: ProcessData | null = null;
        selectedWindow: WindowData | null = null;
        selectedProcessId: number = -1;
        selectedWindowId: number = -1;

        typeDatas: TypeData[] = this.getTypeDatas();
        processData: ProcessData[] = this.getProcessData();
        windowData: WindowData[] = this.getWindowData(this.selectedProcessId);

        getTypeDatas(): TypeData[] {
            return ipcRenderer.sendSync('get-type-data');
        }

        getProcessData(): ProcessData[] {
            return ipcRenderer.sendSync('get-processes-data');
        }

        getWindowData(processId: number): WindowData[] {
            return ipcRenderer.sendSync('get-windows-data', processId);
        }

        clickProcess(process: ProcessData) {
            this.selectedProcess = process;
            this.selectedProcessId = process.process_id;
            this.selectedWindow = null;
            this.selectedWindowId = -1;
            this.windowData = this.getWindowData(this.selectedProcessId);
        }

        clickWindow(window: WindowData) {
            this.selectedWindow = window;
            this.selectedWindowId = window.window_id;
        }

        timeAsString(time: number): string {
            let hours = Math.floor(time / 60 / 60);
            let minutes = Math.floor((time - hours * 60 * 60) / 60);
            let seconds = time - hours * 60 * 60 - minutes * 60;

            if (hours > 0) {
                return `${hours}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
            } else if (minutes > 0) {
                return `${minutes}:${seconds.toString().padStart(2, "0")}`
            } else {
                return `${seconds}`
            }
        }

        update(): void {
            this.processData = this.getProcessData();
            this.windowData = this.getWindowData(this.selectedProcessId);
        }

        getTypesBesides(type: string): TypeData[] {
            return this.typeDatas.filter(typeData => typeData.type !== type);
        }

        async setWindowType(event: Event) {
            // @ts-ignore
            ipcRenderer.sendSync('set-window-type', this.selectedWindowId, event.target.value);
            this.update();
        }

        async setProcessType(event: Event) {
            // @ts-ignore
            ipcRenderer.sendSync('set-process-type', this.selectedProcessId, event.target.value);
            this.update();
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    #processes {
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: 2fr 5fr;
        height: 100%;
    }

    #infoSection {
        grid-column: 1 / 2;
        grid-row: 1 / 2;
    }

    #tableSection {
        grid-column: 1 / 2;
        grid-row: 2 / 3;
        overflow: auto;
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr;
    }

    .section {
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 5px 5px 5px grey;
        background-color: white;
    }

    #processTableSection {
        margin-right: 5px;
        grid-column: 1 / 2;
        overflow: auto;
    }

    #processTable {
        table-layout: fixed;
    }

    #windowTableSection {
        margin-left: 5px;
        grid-column: 2 / 3;
        overflow: auto;
    }

    #windowTable {
        table-layout: fixed;
    }

    td {
        white-space: nowrap;
        overflow: hidden;
    }

    tr.hover:hover {
        background-color: #D9D9D9;
    }

    .selected,
    tr.hover.selected:hover {
        background-color: #C3C3C3C3;
    }

    .timeHeader {
        width: 80px;
    }
</style>