<template>
    <div class="navigationItem">
        <img alt="Timechart logo" src="../assets/icon.png">
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';

    @Component
    export default class NavigationItem extends Vue {
    }
</script>

<style scoped>
    img {
        max-width: 100%;
    }

    .navigationItem {
        resize: both;
        /*background-color: #3D4A63;*/
    }
</style>
