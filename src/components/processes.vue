<template>
    <div id="processes">
        <div id="dateSelectionSection" class="topSection is-vertical-center">
            <date-selection
                    :range="range"
                    @updateRange="updateRange"
            />
        </div>
        <div class="section" id="infoSection">
            <div v-if="selectedWindow !== null">
                <span class="bold">Window: </span>
                <span class="selectable">{{selectedWindow.title}}</span>
            </div>
            <div v-else-if="selectedProcess !== null">
                <span class="bold">Path: </span>
                <span class="selectable">{{selectedProcess.path}}</span>
            </div>

            <div v-if="selectedProcess !== null">
                <span class="bold">Process: </span>
                <span class="selectable">{{selectedProcess.name}}</span>
            </div>

            <div v-if="selectedWindow !== null">
                <span class="bold">Time: </span>
                <span>{{timeAsString(selectedWindow.time)}}</span>
            </div>
            <div v-else-if="selectedProcess !== null">
                <span class="bold">Time: </span>
                <span>{{timeAsString(selectedProcess.time)}}</span>
            </div>

            <div v-if="selectedWindow !== null">
                <label class="bold" for="windowTypeSelection">Type: </label>
                <select id="windowTypeSelection" :style="{color: selectedWindow.color}" @change="setWindowType">
                    <option :value="selectedWindow.type" :style="{color: selectedWindow.color}">
                        {{selectedWindow.type}}
                    </option>
                    <option v-for="typeData in getTypesBesides(selectedWindow.type)"
                            :key="typeData.type" :value="typeData.type"
                            :style="{color: typeData.color}">
                        {{typeData.type}}
                    </option>
                </select>
            </div>
            <div v-else-if="selectedProcess !== null">
                <label class="bold" for="processTypeSelection">Type: </label>
                <select id="processTypeSelection" :style="{color: selectedProcess.color}" @change="setProcessType">
                    <option :value="selectedProcess.type" :style="{color: selectedProcess.color}">
                        {{selectedProcess.type}}
                    </option>
                    <option v-for="typeData in getTypesBesides(selectedProcess.type)"
                            :key="typeData.type" :value="typeData.type"
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
                    <tbody v-for="process in this.processData" :key="process.id" @click="clickProcess(process)">
                    <tr class='hover' :class="{selected: selectedProcessId === process.id}">
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
                    <tbody v-for="window in this.windowData" :key="window.id" @click="clickWindow(window)">
                    <tr class='hover' :class="{selected: selectedWindowId === window.id}">
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
    import {Component, Prop, Watch, Vue} from 'vue-property-decorator';
    import ipcRenderer from '@/components/ipc_renderer';
    import ContentPage from "@/components/contentPage.vue";
    import DateSelection from '@/components/fragments/date_selection.vue';
    import Updatable from "@/components/updatable";
    import {DateRange} from "v-calendar";
    import {formatSeconds} from "@/util/time_util";

    declare interface ProcessData {
        id: number,
        path: string,
        name: string,
        time: number,
        type: string,
        color: string
    }

    declare interface WindowData {
        id: number,
        title: string,
        time: number,
        type: string,
        color: string
    }

    declare interface TypeData {
        type: string,
        color: string
    }

    @Component({
        components: {
            DateSelection
        }
    })
    export default class Processes extends Vue implements ContentPage, Updatable {
        @Prop() range?: DateRange;

        selectedProcess: ProcessData | null = null;
        selectedWindow: WindowData | null = null;
        selectedProcessId: number = -1;
        selectedWindowId: number = -1;

        typeDatas: TypeData[] = this.getTypeDatas();
        processData: ProcessData[] = this.getProcessData();
        windowData: WindowData[] = this.getWindowData(this.selectedProcessId);

        mounted() {
            if (this.processData.length > 0) {
                this.selectedProcess = this.processData[0];
                this.selectedProcessId = this.selectedProcess.id;
                this.windowData = this.getWindowData(this.selectedProcessId);
            }
        }

        getTypeDatas(): TypeData[] {
            return ipcRenderer.sendSync('get-type-data');
        }

        getProcessData(): ProcessData[] {
            return ipcRenderer.sendSync('get-processes-data',
                this.range!.start.getTime(), this.range!.end.getTime());
        }

        getWindowData(processId: number): WindowData[] {
            return ipcRenderer.sendSync('get-windows-data',
                this.range!.start.getTime(), this.range!.end.getTime(), processId);
        }

        clickProcess(process: ProcessData) {
            this.selectedProcess = process;
            this.selectedProcessId = process.id;
            this.selectedWindow = null;
            this.selectedWindowId = -1;
            this.windowData = this.getWindowData(this.selectedProcessId);
        }

        clickWindow(window: WindowData) {
            this.selectedWindow = window;
            this.selectedWindowId = window.id;
        }

        timeAsString(time: number): string {
            return formatSeconds(time);
        }

        update(): void {
            this.processData = this.getProcessData();
            this.windowData = this.getWindowData(this.selectedProcessId);

            this.selectedProcess = this.getSelectedProcess();
            this.selectedWindow = this.getSelectedWindow();
        }

        getTypesBesides(type: string): TypeData[] {
            return this.typeDatas.filter(typeData => typeData.type !== type);
        }

        async setWindowType(event: Event) {
            // @ts-ignore
            let type = event.target.value;

            if (type === 'unknown') {
                type = null;
            }

            ipcRenderer.sendSync('set-window-type', this.selectedWindowId, type);
            this.update();
        }

        async setProcessType(event: Event) {
            // @ts-ignore
            ipcRenderer.sendSync('set-process-type', this.selectedProcessId, event.target.value);
            this.update();
        }

        getSelectedProcess(): ProcessData | null {
            let process = this.processData.find((process: ProcessData) => process.id == this.selectedProcessId);

            if (process !== undefined) {
                return process;
            } else {
                return null;
            }
        }

        getSelectedWindow(): WindowData | null {
            let window = this.windowData.find((window: WindowData) => window.id == this.selectedWindowId);

            if (window !== undefined) {
                return window;
            } else {
                return null;
            }
        }

        updateRange(range: DateRange) {
            this.$emit('updateRange', range);
        }

        @Watch("range")
        onDateChange() {
            this.update()
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    #processes {
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: 40px 2fr 5fr;
        height: 100%;
        margin-left: 10px;
    }

    #infoSection {
        grid-column: 1 / 2;
        grid-row: 2 / 3;
    }

    #tableSection {
        grid-column: 1 / 2;
        grid-row: 3 / 4;
        overflow: auto;
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr;
    }

    .section {
        padding: 10px;
        margin: 0 10px 10px 0;
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

    .topSection {
        margin: 10px 10px 10px 0;
    }

    .is-vertical-center {
        display: flex;
        align-items: center;
        justify-content: space-between
    }

    td {
        white-space: nowrap;
        overflow: hidden;
    }

    .selected {
        background-color: #F1F1F1;
    }

    tr.hover:hover {
        background-color: #EAEAEA;
    }

    .timeHeader {
        width: 80px;
    }
</style>
