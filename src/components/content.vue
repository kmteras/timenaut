<template>
    <div class="content">
        <component :is=page></component>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';


    @Component
    export default class AppContent extends Vue {
        @Prop() page!: Vue;
    }
</script>
