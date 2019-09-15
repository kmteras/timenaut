<template>
    <div>
        <p v-on:click='Focused = !Focused' v-on-clickaway="clickedaway">Options</p>
        <div v-bind:class="{focused : !Focused}">Hello options!</div>
    </div>
</template>

<script>
    import {mixin as clickaway} from 'vue-clickaway'

    export default ({
        mixins: [clickaway],
        data() {
            return {
                Focused: false
            }
        },
        methods: {
            clickedaway() {
                this.Focused = false;
            }
        }
    })
</script>

<style scoped>
    .focused {
        visibility: hidden;
    }
</style>
<!--<template>
    <div v-bind:class="{ 'is-active': isDropdownActive }" v-on-clickaway="away">
        <div  @click="isDropdownActive=!isDropdownActive">
            <a aria-haspopup="true" aria-controls="{ 'dropdown-menu'}">
                <span>More</span>
                <span >
                  <i aria-hidden="true"></i>
                </span>
            </a>
        </div>
        <div  id="dropdown-menu" role="menu">
            <div >
                <a href="#">
                    <span>Some Action</span>
                </a>
            </div>
        </div>
    </div>
</template>

<script>
    import { mixin as clickaway } from 'vue-clickaway';
    export default {
        props: ['id'],
        mixins: [ clickaway ],
        data() {
            return {
                isDropdownActive: false,
            }
        },
        methods: {
            away() {
                this.isDropdownActive = false;
            }
        }
    };
</script>

<style scoped>
</style>-->