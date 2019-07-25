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
