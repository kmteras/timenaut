<template>
    <div class="navigation">
        <navigation-logo/>
        <div v-for="item in items" v-bind:key="item.icon">
            <navigation-item :icon=item.icon :iconAlt=item.iconAlt :switchPage="switchPage"
                             :page="item.page"/>
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';
    import NavigationLogo from "@/components/fragments/navigation_logo.vue";
    import NavigationItem from "@/components/fragments/navigation_item.vue";

    @Component({
        components: {NavigationItem, NavigationLogo}
    })
    export default class Navigation extends Vue {
        @Prop() private items!: object;
        @Prop() switchPage!: any;
    }
</script>

<style scoped>
    .navigation {
        padding-top: 10px;
        background-color: #3D4A63;
        display: flex;
        flex-direction: column;
    }
</style>
