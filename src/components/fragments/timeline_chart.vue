<script lang="ts">
    import {Bar} from 'vue-chartjs';
    import ipcRenderer from '@/components/ipc_renderer';
    import {DateRange} from "v-calendar";
    import {Chart, ChartData, ChartLegendLabelItem} from 'chart.js'

    import {Component, Mixins, Prop, Provide, Watch} from 'vue-property-decorator';

    @Component
    export default class Timeline extends Mixins(Bar) {
        @Provide() data: ChartData = this.getTimelineData();
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
                        xAxes: [{
                            stacked: true,
                            ticks: {
                                maxTicksLimit: 25
                            }
                        }],
                        yAxes: [{
                            stacked: true,
                            ticks: {
                                min: 0,
                                max: 600
                            }
                        }]
                    },
                    legend: {
                        onClick: this.onLegendCallback
                    }
                });
        }

        getTimelineData() {
            return ipcRenderer.sendSync('get-timeline-data', this.range!.start.getTime());
        }

        @Watch("range")
        onDateChange() {
            this.update()
        }

        onLegendCallback(e: MouseEvent, legend: ChartLegendLabelItem) {
            Chart.defaults.global.legend!.onClick!.call(this.$data._chart, e, legend);
            this.$data._chart.update();
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
