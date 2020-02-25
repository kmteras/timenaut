<script lang="ts">
    import {Doughnut} from 'vue-chartjs';
    import ipcRenderer from '@/components/ipc_renderer';
    import {DateRange} from "v-calendar";
    import {ChartData} from 'chart.js';

    import {Component, Mixins, Prop, Provide, Watch} from 'vue-property-decorator';
    import {formatSeconds} from "@/util/time_util";

    @Component
    export default class DailyPieChart extends Mixins(Doughnut) {
        @Provide() data: ChartData = this.getData();
        @Prop() date?: Date;
        @Prop() range?: DateRange;

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
                    legend: {
                        position: "right",
                        align: "center"
                    },
                    scales: {
                        xAxes: [{
                            gridLines: {
                                display: false,
                                drawBorder: false
                            },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                            gridLines: {
                                display: false,
                                drawBorder: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    },
                    tooltips: {
                        callbacks: {
                            label: (t: any, d: any) => {
                                let totalSeconds = d.datasets[t.datasetIndex].data[t.index];
                                return formatSeconds(totalSeconds);
                            }
                        }
                    }
                });
        }

        getData() {
            return ipcRenderer.sendSync('get-pie-data', this.range!.start.getTime(), this.range!.end.getTime());
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
