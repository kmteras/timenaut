<script lang="ts">
    import {Doughnut} from 'vue-chartjs';
    import {ipcRenderer} from 'electron';

    import {Component, Mixins, Provide} from 'vue-property-decorator';

    @Component
    export default class DailyPieChart extends Mixins(Doughnut) {
        @Provide() data: object = DailyPieChart.getData();

        mounted() {
            this.renderChart(this.data,
                {
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
                                let hours = Math.floor(totalSeconds / 60 / 60);
                                let minutes = Math.floor((totalSeconds - hours * 60 * 60) / 60);
                                let seconds = totalSeconds - hours * 60 * 60 - minutes * 60;

                                if (hours > 0) {
                                    return `${hours}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
                                } else if (minutes > 0) {
                                    return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
                                } else {
                                    return `${seconds.toString().padStart(2, "0")}`
                                }
                            }
                        }
                    }
                });
        }

        static getData() {
            return ipcRenderer.sendSync('get-pie-data');
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
