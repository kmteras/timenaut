<template>
    <div id="dashboard">
        <div id="dateSelectionSection" class="topSection is-vertical-center">
            <date-selection
                    :range="range"
                    @updateRange="updateRange"
            />
        </div>

        <div class="section" id="timelineSection">
            <timeline :height="250" :range="range" ref="timeline" :class="{'hidden': !showDailyTimeline()}"/>
            <daily-timeline :height="250" :range="range" ref="timeline" :class="{'hidden': showDailyTimeline()}"/>
        </div>

        <div class="section" id="pieSection">
            <daily-pie-chart :height="200" :width="200" :range="range" ref="pieChart"/>
        </div>

        <div class="section" id="barSection">
            <process-graph :height="200" :width="200" :range="range" ref="processChart"/>
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';
    import Timeline from '@/components/fragments/timeline_chart.vue';
    import DailyPieChart from '@/components/fragments/daily_pie_chart.vue';
    import DateSelection from '@/components/fragments/date_selection.vue';
    import Updatable from "@/components/updatable";
    import {Calendar, DatePicker, DateRange} from "v-calendar";
    import ProcessGraph from "@/components/fragments/process_graph.vue";
    import DailyTimeline from "@/components/fragments/daily_timeline_chart.vue";

    @Component({
        components: {
            ProcessGraph,
            Timeline,
            DailyTimeline,
            DailyPieChart,
            DateSelection,
            Calendar,
            DatePicker
        }
    })
    export default class Dashboard extends Vue implements Updatable {
        @Prop() range!: DateRange;

        updateRange(range: DateRange) {
            this.$emit('updateRange', range);
        }

        showDailyTimeline(): boolean {
            return this.range.start.getTime() === this.range.end.getTime();
        }

        update(): void {
            // @ts-ignore
            this.$refs.timeline.update();
            // @ts-ignore
            this.$refs.pieChart.update();
            // @ts-ignore
            this.$refs.processChart.update();
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

    .topSection {
        margin: 10px 10px 10px 0;
    }

    .is-vertical-center {
        display: flex;
        align-items: center;
        justify-content: space-between
    }

    .hidden {
        display: none;
    }

    button {
        height: 38px;
    }
</style>
