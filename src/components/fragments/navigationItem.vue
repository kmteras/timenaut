<template>
    <div class="navigationItem">
        <i class="material-icons" v-on:click="pressed">{{icon}}</i>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';

    @Component
    export default class NavigationItem extends Vue {
        @Prop() private icon!: string;
        @Prop() private iconAlt!: string;
        @Prop() private page!: object;
        @Prop() switchPage!: any;

        pressed() {
            this.switchPage(this.page)
        }
    }
</script>

<style scoped>
    i {
        font-size: 40px;
        margin-top: -20px;
        margin-left: -20px;
        position: absolute;
        top: 50%;
        left: 50%;
        color: white;
    }

    i:hover {
        color: black;
    }

    i:active {
        color: grey;
    }

    .navigationItem {
        position: relative;
        resize: both;
        min-height: 60px;
        place-items: center center;
        user-select: none;
    }
</style>
