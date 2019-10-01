<script lang="ts">
    import {Line} from 'vue-chartjs';
    import ipcRenderer from '@/components/ipcRenderer';
    import {DateRange} from "v-calendar";

    import {Component, Mixins, Prop, Provide, Watch} from 'vue-property-decorator';
    import {formatSeconds} from "@/util/timeUtil";

    @Component
    export default class LongTimeline extends Mixins(Line) {
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
                            stacked: true,
                            ticks: {
                                min: 0,
                                maxTicksLimit: 3600,
                                callback: function(value: number) {
                                    return formatSeconds(value);
                                }
                            }
                        }]
                    },
                    tooltips: {
                        callbacks: {
                            label: (t: any, d: any) => {
                                let totalSeconds = d.datasets[t.datasetIndex].data[t.index];
                                if (totalSeconds == 0) {
                                    return null;
                                }

                                return formatSeconds(totalSeconds);
                            }
                        }
                    }
                });
        }

        getTimelineData() {
            return ipcRenderer.sendSync('get-daily-timeline-data', this.range!.start.getTime(), this.range!.end.getTime());
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
