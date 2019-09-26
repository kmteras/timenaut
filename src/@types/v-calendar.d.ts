declare module 'v-calendar' {
    import {Vue} from 'vue-property-decorator';

    export class Calendar extends Vue {

    }

    export class DatePicker extends Vue {

    }

    export interface DateRange {
        start: Date,
        end: Date
    }
}
