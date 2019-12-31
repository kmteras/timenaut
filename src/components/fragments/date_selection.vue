<template>
    <div class="date-selection">
        <div class="is-pulled-left">
            <button class="button is-pulled-left" :class="{'disabled': hasPrevDate()}" @click="shiftRangeLeft">&#8592;
            </button>
            <date-picker
                    class="is-pulled-left"
                    mode="range"
                    @input="updateParent"
                    :value="range"
                    :first-day-of-week="2"
                    :min-date="getFirstDate()"
                    :max-date="getMaxDate()"
            />
            <button class="button" :class="{'hidden': hasNextDate()}" @click="shiftRangeRight">&#8594;</button>
        </div>
        <button class="is-pulled-right button" @click="allTime">All time</button>
        <button class="is-pulled-right button" @click="thisWeek">Week</button>
        <button class="is-pulled-right button" @click="thisMonth">Month</button>
        <button class="is-pulled-right button" @click="today">Today</button>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';
    import ipcRenderer from '@/components/ipc_renderer';
    import {Calendar, DatePicker, DateRange} from "v-calendar";
    import {getDayLength, getNextDate, getPrevDate, getToday} from '@/util/time_util'

    @Component({
        components: {
            Calendar,
            DatePicker
        }
    })
    export default class DateSelection extends Vue {
        @Prop() range?: DateRange;

        shiftRangeLeft() {
            this.updateParent({
                start: getPrevDate(this.range!.start),
                end: getPrevDate(this.range!.end)
            });
        }

        today() {
            this.updateParent({
                start: getToday(),
                end: getToday()
            });
        }

        thisWeek() {
            this.updateParent({
                start: new Date(getToday().getTime() - getDayLength() * 7 * 1000),
                end: getToday()
            });
        }

        thisMonth() {
            this.updateParent({
                start: new Date(getToday().getTime() - getDayLength() * 31 * 1000),
                end: getToday()
            });
        }

        allTime() {
            this.updateParent({
                start: this.getFirstDate(),
                end: this.getMaxDate()
            });
        }

        shiftRangeRight() {
            this.updateParent({
                start: getNextDate(this.range!.start),
                end: getNextDate(this.range!.end)
            });
        }

        updateParent(range: DateRange) {
            this.$emit('updateRange', range);
        }

        hasPrevDate(): boolean {
            return this.range!.start <= this.getFirstDate();
        }

        hasNextDate(): boolean {
            return getNextDate(this.range!.end) > getToday();
        }

        getMaxDate(): Date {
            return getToday();
        }

        getFirstDate(): Date {
            let time = ipcRenderer.sendSync('get-first-date');
            if (time === null) {
                return getToday();
            }
            return new Date(time * 1000);
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .date-selection {
        width: 100%;
    }

    .disabled {
        opacity: 0.5;
    }

    button {
        height: 38px;
    }
</style>
