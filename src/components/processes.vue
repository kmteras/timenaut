<template>
    <div id="processes">
        <div class="section" id="infoSection">
            <h1>Processes</h1>
        </div>
        <div class="section" id="processesSection">
            <div id="processData">
                <table class="table is-narrow">
                    <thead>
                    <tr>
                        <th>Process</th>
                        <th>Time</th>
                    </tr>
                    </thead>
                    <tbody v-for="(process, idx) in this.processData" :key="idx" @click="clickProcess(process)">
                    <tr class='hover' :class="{selected: selectedProcess === process.process_id}">
                        <td :style="{color: process.color}">{{process.name}}</td>
                        <td>{{process.time}}</td>
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

    declare interface ProcessData {
        path: string,
        name: string,
        time: number,
        process_id: number,
        type: string,
        color: string
    }

    @Component
    export default class Processes extends Vue implements ContentPage {
        @Provide() message = 'message';
        selectedProcess: number = -1;

        processData: [ProcessData] = this.getData();

        mounted() {
            ipcRenderer.on('heartbeat', (event: any) => {
                this.processData = this.getData();
            })
        }

        getData(): [ProcessData] {
            return ipcRenderer.sendSync('get-processes-data');
        }

        clickProcess(process: ProcessData) {
            this.selectedProcess = process.process_id;
            console.log(this.selectedProcess);
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

    #processesSection {
        grid-column: 1 / 2;
        grid-row: 2 / 3;
        overflow: auto;
    }

    .section {
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 5px 5px 5px grey;
        background-color: white;
    }

    #processData {
        overflow: auto;
    }

    tr.hover:hover {
        background-color: #D9D9D9;
    }

    .selected,
    tr.hover.selected:hover {
        background-color: #C3C3C3C3;
    }
</style>
