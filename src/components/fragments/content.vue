<template>
    <div class="content">
        <component :is=page ref="component" :range="range" @updateRange="updateRange"></component>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Provide, Vue} from 'vue-property-decorator';
    import ipcRenderer from '@/components/ipc_renderer';
    import {DateRange} from "v-calendar";
    import {getToday} from "@/util/time_util";

    @Component
    export default class AppContent extends Vue {
        @Prop() page!: Vue;

        @Provide() range: DateRange = {
            start: getToday(),
            end: getToday()
        };

        mounted() {
            ipcRenderer.on('heartbeat', this.update.bind(this))
        }

        updateRange(range: DateRange) {
            this.range = range;
        }

        update() {
            // @ts-ignore
            if (this.$refs.component.update) {
                // @ts-ignore
                this.$refs.component.update();
            }
        }
    }
</script>
