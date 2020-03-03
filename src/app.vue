<template>
    <div id="app" class="content">
        <navigation id="navigation" :items=navigationItems :switchPage="switchPage"/>
        <app-content id="content" :page="page"/>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import AppContent from '@/components/fragments/content.vue';
    import Navigation from '@/components/fragments/navigation.vue';
    import Dashboard from "@/components/dashboard.vue";
    import Processes from "@/components/processes.vue";
    import Settings from "@/components/settings.vue";
    import Updatable from "@/components/updatable";

    interface PageComponent {
        new(): Updatable;
    }

    type NavigationItem = {
        icon: string,
        iconAlt: string,
        page: PageComponent
    }

    @Component({
        components: {
            Navigation,
            AppContent,
        },
    })
    export default class App extends Vue {
        page: PageComponent = Dashboard;

        navigationItems: NavigationItem[] = [
            {icon: 'dashboard', iconAlt: 'dashboard', page: Dashboard},
            {icon: 'query_builder', iconAlt: 'processes', page: Processes},
            {icon: 'settings', iconAlt: 'settings', page: Settings}
        ];

        switchPage(newPage: PageComponent) {
            this.page = newPage;
        }
    }
</script>

<style>
    @font-face {
        font-family: "Montserrat";
        src: url("assets/fonts/Montserrat-Regular.ttf") format("truetype");
    }

    html {
        height: 100%;
        overflow-x: hidden !important;
        overflow-y: hidden !important;
        user-select: none;
    }

    body {
        margin: 0;
        background-color: #D9D9D9;
        min-height: 100%;
        max-height: 100%;
    }

    html, body, button, input, select, textarea {
        font-family: Montserrat, 'Avenir', Helvetica, Arial, sans-serif !important;
    }

    #app {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-bottom: 0;
        height: 100%;
    }

    #app {
        display: grid;
        grid-template-columns: 60px auto;
        grid-template-rows: 100%;
        height: 100vh;
    }

    #navigation {
        position: fixed;
        width: 60px;
        height: 100%;
    }

    #content {
        grid-column: 2 / 3;
    }

    .selectable {
        user-select: text;
    }

    .bold {
        font-weight: bold;
    }

    input[type=text],
    input[type=number],
    input[type=password] {
        padding-top: 8px;
        padding-bottom: 8px;
        border-width: 1px;
        border-radius: 4px;
        border-color: #cbd5e0;
        border-style: solid;
        line-height: 1.25;
        color: #2d3748;
        font-size: 16px;
        padding-left: 12px;
        padding-right: 12px;
        margin-left: 10px;
        height: 36px;
    }

    input[type=checkbox] {
        margin-left: 12px;
        position: absolute;
        cursor: pointer;
        width: 18px;
        height: 18px;
    }

</style>
