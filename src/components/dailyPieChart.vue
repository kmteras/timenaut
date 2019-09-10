<template>
    <svg height="100%" width="100%">
        <g transform="">

        </g>
    </svg>
</template>
<script lang="ts">
    import {ipcRenderer} from 'electron';
    import {Component, Prop, Provide, Vue, Watch} from 'vue-property-decorator';

    @Component
    export default class DailyPieChart extends Vue {
        @Provide() data: { datasets: {}, labels: {} } = this.getData();
        @Prop() date?: Date;

        mounted() {
            this.drawChart(true);
        }

        update(): any {
            // TODO: update graph somehow so it does not refresh everything
            // TODO: if this tab is in focus
            this.data = this.getData();
            this.drawChart(false);
        }

        drawChart(animation: boolean) {

        }

        getData() {
            return ipcRenderer.sendSync('get-pie-data', this.date!.getTime());
        }

        @Watch("date")
        onDateChange() {
            this.update()
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
