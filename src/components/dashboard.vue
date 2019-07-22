<template>
    <div id="dashboard">
        <div class="section" id="timelineSection">
            <timeline :height="280"/>
        </div>

        <div class="section" id="otherSection">
            <img alt="Vue logo" src="../assets/logo.png">

            <h1>{{ message }}</h1>
            <button id="testbutton" @click="clickTest">Test</button>
            <p>
                For a guide and recipes on how to configure / customize this project,<br>
                check out the
                <a href="https://cli.vuejs.org" target="_blank" rel="noopener">vue-cli documentation</a>.
            </p>
            <h3>Installed CLI Plugins</h3>
            <ul>
                <li><a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-typescript"
                       target="_blank" rel="noopener">typescript</a></li>
            </ul>
            <h3>Essential Links</h3>
            <ul>
                <li><a href="https://vuejs.org" target="_blank" rel="noopener">Core Docs</a></li>
                <li><a href="https://forum.vuejs.org" target="_blank" rel="noopener">Forum</a></li>
                <li><a href="https://chat.vuejs.org" target="_blank" rel="noopener">Community Chat</a></li>
                <li><a href="https://twitter.com/vuejs" target="_blank" rel="noopener">Twitter</a></li>
                <li><a href="https://news.vuejs.org" target="_blank" rel="noopener">News</a></li>
            </ul>
            <h3>Ecosystem</h3>
            <ul>
                <li><a href="https://router.vuejs.org" target="_blank" rel="noopener">vue-router</a></li>
                <li><a href="https://vuex.vuejs.org" target="_blank" rel="noopener">vuex</a></li>
                <li><a href="https://github.com/vuejs/vue-devtools#vue-devtools" target="_blank"
                       rel="noopener">vue-devtools</a></li>
                <li><a href="https://vue-loader.vuejs.org" target="_blank" rel="noopener">vue-loader</a></li>
                <li><a href="https://github.com/vuejs/awesome-vue" target="_blank" rel="noopener">awesome-vue</a></li>
            </ul>
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Provide, Vue} from 'vue-property-decorator';
    import {ipcRenderer} from 'electron';
    import Timeline from '@/components/timelineChart.vue';

    @Component({
        components: {
            Timeline
        }
    })
    export default class Dashboard extends Vue {
        @Prop() private msg!: string;

        // @Inject() message!: string;
        @Provide() message = 'message';

        clickTest() {
            this.message = ipcRenderer.sendSync('synchronous-message');
        }

    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    #dashboard {
        display: grid;
        grid-template-columns: 200px auto;
        grid-template-rows: 300px auto;
    }

    #timelineSection {
        grid-column: 1 / 3;
        grid-row: 1 / 2;
    }

    #otherSection {
        grid-column: 1 / 3;
        grid-row: 2 / 3;
    }

    .section {
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 5px 5px 5px grey;
        background-color: white;
    }
</style>
