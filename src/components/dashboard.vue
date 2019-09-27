<template>
    <div id="dashboard">
        <div id="dateSelectionSection" class="topSection is-vertical-center">
            <date-selection
                    :range="range"
                    @updateRange="updateRange"
            />
        </div>

        <div class="section" id="timelineSection">
            <timeline :height="250" :range="range" ref="timeline"/>
        </div>

        <div class="section" id="pieSection">
            <daily-pie-chart :height="200" :width="200" :range="range" ref="pieChart"/>
        </div>

        <div class="section" id="barSection">
            <!--<daily-pie-chart />-->
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';
    import Timeline from '@/components/fragments/timelineChart.vue';
    import DailyPieChart from '@/components/fragments/dailyPieChart.vue';
    import DateSelection from '@/components/fragments/dateSelection.vue';
    import Updatable from "@/components/updatable";
    import {Calendar, DatePicker, DateRange} from "v-calendar";

    @Component({
        components: {
            Timeline,
            DailyPieChart,
            DateSelection,
            Calendar,
            DatePicker
        }
    })
    export default class Dashboard extends Vue implements Updatable {
        @Prop() range?: DateRange;

        updateRange(range: DateRange) {
            this.$emit('updateRange', range);
        }

        update(): void {
            // @ts-ignore
            this.$refs.timeline.update();
            // @ts-ignore
            this.$refs.pieChart.update();
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    #dashboard {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 40px 52% 40%;
        height: 100%;
        margin-left: 10px;
    }

    #dateSelectionSection {
        grid-column: 1 / 3;
        grid-row: 1 / 2;
    }

    #timelineSection {
        margin-top: 0;
        grid-column: 1 / 3;
        grid-row: 2 / 3;
    }

    #pieSection {
        grid-column: 1 / 2;
        grid-row: 3 / 4;
    }

    #barSection {
        grid-column: 2 / 3;
        grid-row: 3 / 4;
    }

    .section {
        padding: 10px 10px 0 10px;
        margin: 0 10px 10px 0;
        border-radius: 10px;
        box-shadow: 5px 5px 5px grey;
        background-color: white;
    }

    .topSection {
        margin: 10px 10px 10px 0;
    }

    .is-vertical-center {
        display: flex;
        align-items: center;
        justify-content: space-between
    }

    .hidden {
        visibility: hidden;
    }

    button {
        height: 38px;
    }
</style>
