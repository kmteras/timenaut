<template>
    <div class="settings">
        <h1>Settings</h1>
    </div>
</template>

<script lang="ts">
    import {Provide, Inject, Component, Prop, Vue} from 'vue-property-decorator';
    import {ipcRenderer} from 'electron';

    @Component
    export default class Settings extends Vue {
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
