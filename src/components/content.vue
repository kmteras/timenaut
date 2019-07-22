<template>
    <div class="content">
        <component :is=page></component>
    </div>
</template>

<script lang="ts">
    import {Provide, Inject, Component, Prop, Vue} from 'vue-property-decorator';
    import {ipcRenderer} from 'electron';
    import Dashboard from "@/components/dashboard.vue";


    @Component
    export default class AppContent extends Vue {
        @Prop() page!: Vue;
        // @Provide() page = Dashboard;
        // clickTest() {
        //     this.message = ipcRenderer.sendSync('synchronous-message');
        // }

        // page() {
        //     return "dashboard"
        // }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    h3 {
        margin: 40px 0 0;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        display: inline-block;
        margin: 0 10px;
    }

    a {
        color: #42b983;
    }
</style>
