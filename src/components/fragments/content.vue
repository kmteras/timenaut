<template>
    <div class="content">
        <component :is=page ref="component"></component>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';
    import ipcRenderer from '@/components/ipcRenderer';

    @Component
    export default class AppContent extends Vue {
        @Prop() page!: Vue;

        mounted() {
            ipcRenderer.on('heartbeat', this.update.bind(this))
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
