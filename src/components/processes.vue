<template>
    <div id="processes">
        <div class="section" id="infoSection">
            <h1>Processes</h1>
        </div>
        <div class="section" id="processesSection"></div>
    </div>
</template>

<script lang="ts">
    import {Provide, Inject, Component, Prop, Vue} from 'vue-property-decorator';
    import {ipcRenderer} from 'electron';

    @Component
    export default class Processes extends Vue {
        @Provide() message = 'message';

        clickTest() {
            this.message = ipcRenderer.sendSync('synchronous-message');
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
    }

    .section {
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 5px 5px 5px grey;
        background-color: white;
    }
</style>
