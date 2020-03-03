<template>
    <div class="template">
        <div v-if="this.selected !== undefined" class="tn-select" @click="toggle" :class="{open: open}">
            <div :style="{color: getColor(this.selected)}">{{getString(this.selected)}}<i :class="{open: open}"></i>
            </div>
        </div>
        <div v-if="this.open" class="tn-select-options">
            <div v-for="element in this.elements" :key="element.value">
                <div :style="{color: getColor(element)}" class="tn-select-option" @click="select(element)">
                    {{getString(element)}}
                </div>
            </div>
        </div>
        <div v-if="this.open" class="tn-select-overlay" @click="toggle"></div>
    </div>
</template>
<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';
    import log from "electron-log";

    @Component({
        name: 'TnSelect'
    })
    export default class TnSelect extends Vue {
        @Prop() elements?: any;
        @Prop() selected?: any;

        @Prop() valueKey?: string;
        @Prop() colorKey?: string;

        @Prop() change?: (event: any) => any;

        private open: boolean = false;

        private getString(element: any) {
            if (this.valueKey === undefined) {
                return undefined;
            }
            return element[this.valueKey];
        }

        private getColor(element: any) {
            if (this.colorKey === undefined) {
                return 'black';
            }

            const color = element[this.colorKey];
            if (color !== undefined) {
                return color;
            }
            return 'black';
        }

        private toggle() {
            this.open = !this.open;
        }

        private select(element: any) {
            log.debug(element);
            log.debug(this.change);
            if (this.change !== undefined) {
                this.change(element);
            }
            this.selected = element;
            this.open = false;
        }
    }
</script>
<style scoped>
    .template {
        display: inline-block;
        margin-left: 10px;
    }

    .tn-select {
        padding: 6px 10px 6px 10px;

        border-width: 1px;
        border-radius: 4px;
        border-color: #cbd5e0;
        border-style: solid;
        color: #2d3748;
        font-size: 14px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .1), 0 1px 2px 0 rgba(0, 0, 0, .06);
        height: 36px;
    }

    .tn-select.open {
        border-radius: 4px 4px 0 0;
    }

    .tn-select-options {
        position: absolute;
        background-color: white;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .1), 0 1px 2px 0 rgba(0, 0, 0, .06);

        border-width: 1px;
        border-radius: 4px;
        border-color: #cbd5e0;
        border-style: solid;

        z-index: 101;
    }

    .tn-select-option {
        padding: 4px 10px 4px 10px;
        font-size: 14px;
    }

    .tn-select:hover,
    .tn-select:active,
    .tn-select-option:hover,
    .tn-select-option:active {
        background-color: #EAEAEA;
    }

    .tn-select-overlay {
        position: fixed;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        z-index: 100;
    }

    i {
        margin-left: 8px;
        border: solid #2d3748;
        border-width: 0 2px 2px 0;
        display: inline-block;
        padding: 2px;
        margin-bottom: 1px;
        transform: rotate(45deg);
    }

    i.open {
        transform: rotate(-135deg);
    }
</style>
