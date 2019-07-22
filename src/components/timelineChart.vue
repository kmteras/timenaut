<script lang="ts">
    import {Bar} from 'vue-chartjs';
    import {ipcRenderer} from 'electron';

    import {Component, Mixins, Prop, Provide} from 'vue-property-decorator';

    @Component
    export default class Timeline extends Mixins(Bar) {
        @Provide() data: object = this.getTimelineData();

        mounted() {
            this.renderChart(this.data,
                {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        xAxes: [{
                            stacked: true,
                            ticks: {
                                maxTicksLimit: 25
                            }
                        }],
                        yAxes: [{stacked: true}]
                    }
                });
        }

        getTimelineData() {
            return ipcRenderer.sendSync('get-timeline-data');
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
