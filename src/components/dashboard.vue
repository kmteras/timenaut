<template>
    <div id="dashboard">
        <div id="dateSelectionSection" class="topSection is-vertical-center">
            <span class="is-pulled-left">{{date.toDateString()}}</span>
            <div class="is-pulled-right">
                <button class="button" v-on:click="prevDate">&#8592;</button>
                <button class="button" v-on:click="today">Today</button>
                <button class="button" :class="{'hidden': hasNextDate()}" v-on:click="nextDate">&#8594;</button>
            </div>
        </div>

        <div class="section" id="timelineSection">
            <timeline :date="date" ref="timeline"/>
        </div>

        <div class="section" id="pieSection">
            <daily-pie-chart :date="date" ref="pieChart"/>
        </div>

        <div class="section" id="barSection">
            <!--<daily-pie-chart />-->
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Provide, Vue} from 'vue-property-decorator';
    import Timeline from '@/components/timelineChart.vue';
    import DailyPieChart from '@/components/dailyPieChart.vue';
    import {Updateable} from "@/components/Updateable";

    @Component({
        components: {
            Timeline,
            DailyPieChart
        }
    })
    export default class Dashboard extends Vue implements Updateable {
        @Provide() date: Date = this.getToday();

        prevDate() {
            this.date = this.getPrevDate();
        }

        today() {
            this.date = this.getToday();
        }

        nextDate() {
            this.date = this.getNextDate();
        }

        hasNextDate(): boolean {
            return this.getNextDate() > this.getToday();
        }

        // TODO: get prev matching date from databse
        private getPrevDate(): Date {
            return new Date(this.date.getTime() - 24 * 60 * 60 * 1000);
        }

        private getToday(): Date {
            let date: Date = new Date();
            return new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
        }

        // TODO: get next matching date from databse
        private getNextDate(): Date {
            return new Date(this.date.getTime() + 24 * 60 * 60 * 1000);
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
        grid-template-rows: 40px 1fr 1fr;
        height: 100%;
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
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 5px 5px 5px grey;
        background-color: white;
    }

    .topSection {
        margin: 5px 10px 5px 10px;
    }

    .is-vertical-center {
        display: flex;
        align-items: center;
        justify-content: space-between
    }

    .hidden {
        visibility: hidden;
    }
</style>
