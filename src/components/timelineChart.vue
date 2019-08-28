<script lang="ts">
    import {Bar} from 'vue-chartjs';
    import {ipcRenderer} from 'electron';

    import {Component, Mixins, Prop, Provide, Watch} from 'vue-property-decorator';

    @Component
    export default class Timeline extends Mixins(Bar) {
        @Provide() data: object = this.getTimelineData();
        @Prop() date?: Date;

        mounted() {
            this.drawChart(true);

            ipcRenderer.on('heartbeat', this.update.bind(this))
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
                                // max: 600
                            }
                        }]
                    }
                });
        }

        getTimelineData() {
            return ipcRenderer.sendSync('get-timeline-data', this.date!.getTime());
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
