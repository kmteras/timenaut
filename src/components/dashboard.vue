<template>
    <div id="dashboard">
        <div class="section" id="timelineSection">
            <timeline :height="280"/>
        </div>

        <div class="section" id="pieSection">
            <daily-pie-chart :height="230" :width="200"/>
        </div>

        <div class="section" id="barSection">
<!--            <daily-pie-chart />-->
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Provide, Vue} from 'vue-property-decorator';
    import {ipcRenderer} from 'electron';
    import Timeline from '@/components/timelineChart.vue';
    import DailyPieChart from '@/components/dailyPieChart.vue';

    @Component({
        components: {
            Timeline,
            DailyPieChart
        }
    })
    export default class Dashboard extends Vue {
        @Prop() private msg!: string;

        // @Inject() message!: string;
        @Provide() message = 'message';

        clickTest() {
            this.message = ipcRenderer.sendSync('synchronous-message');
        }

    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    #dashboard {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 300px auto;
    }

    #timelineSection {
        grid-column: 1 / 3;
        grid-row: 1 / 2;
    }

    #pieSection {
        grid-column: 1 / 2;
        grid-row: 2 / 3;
    }

    #barSection {
        grid-column: 2 / 3;
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
