<template>
    <div class="content">
        <h1>Processes</h1>
    </div>
</template>

<script lang="ts">
    import {Provide, Inject, Component, Prop, Vue} from 'vue-property-decorator';
    import {ipcRenderer} from 'electron';

    @Component
    export default class Processes extends Vue {
        @Provide() message = 'message';

        clickTest() {
            this.message = ipcRenderer.sendSync('synchronous-message');
        }
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
