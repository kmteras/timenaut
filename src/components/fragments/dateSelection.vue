<template>
    <div class="date-selection">
        <div class="is-pulled-left">
            <button class="button is-pulled-left" @click="shiftRangeLeft">&#8592;</button>
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
        <button class="is-pulled-right button" @click="today">Today</button>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';
    import ipcRenderer from '@/components/ipcRenderer';
    import {Calendar, DatePicker, DateRange} from "v-calendar";
    import {getNextDate, getPrevDate, getToday} from '@/util/timeUtil'

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

        shiftRangeRight() {
            this.updateParent({
                start: getNextDate(this.range!.start),
                end: getNextDate(this.range!.end)
            });
        }

        updateParent(range: DateRange) {
            this.$emit('updateRange', range);
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

    .hidden {
        visibility: hidden;
    }

    button {
        height: 38px;
    }
</style>
