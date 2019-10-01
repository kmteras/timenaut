<script lang="ts">
    import {HorizontalBar} from 'vue-chartjs';
    import ipcRenderer from '@/components/ipcRenderer';
    import {DateRange} from "v-calendar";

    import {Component, Mixins, Prop, Provide, Watch} from 'vue-property-decorator';

    @Component
    export default class ProcessGraph extends Mixins(HorizontalBar) {
        @Provide() data: object = this.getTimelineData();
        @Prop() date?: Date;
        @Prop() range?: DateRange;

        mounted() {
            this.drawChart(true);
        }

        update(): any {
            // TODO: update graph somehow so it does not refresh everything
            // TODO: if this tab is in focus
            this.data = this.getTimelineData();
            this.drawChart(false);
        }

        drawChart(animation: boolean) {
            this.renderChart(this.data,
                {
                    animation: {
                        duration: animation ? 1000 : 0
                    },
                    hover: {
                        animationDuration: animation ? 400 : 0
                    },
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        yAxes: [{
                            stacked: true
                        }]
                    }
                });
        }

        getTimelineData() {
            return ipcRenderer.sendSync('get-process-graph-data',
                this.range!.start.getTime(),
                this.range!.end.getTime());
        }

        @Watch("range")
        onDateChange() {
            this.update()
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
