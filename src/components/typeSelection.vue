<template>
    <div class="typeSelection" >
        <div class="selectedItem" v-on:click='focused = !focused' v-on-clickaway="clickedaway">{{ selectedItem }}
            <div class="menuItemContainer" v-bind:class="{isFocused : !focused}">
                <div v-for="item in items" class="menuItem" v-bind:key="item.id" v-on:click="setSelectedItem(item)">{{ item }}</div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { mixin as clickaway} from 'vue-clickaway';

    import {Mixins ,Component, Prop} from 'vue-property-decorator';

    @Component
    export default class typeSelection extends Mixins(clickaway) {
        focused: boolean = false;
        items: string[] = ["Cat", "Dog", "Turtle"];
        selectedItem: string =  "Focused";

        clickedaway(): void {
            this.focused = false;
        }

        setSelectedItem(item: string): void {
            this.selectedItem = item;
            // eslint-disable-next-line no-console
            console.log(item);
        }
    }
</script>

<style scoped>
    .typeSelection {
        width: fit-content;
        padding: 0;
        overflow: visible;
        margin: auto;
        position: absolute;
    }

    .isFocused {
        display: none;
    }

    .menuItemContainer {
        overflow: auto;
        height: 100px;
    }
    .menuItem {
        background: white;
        text-align: left;
    }

    .selectedItem {
        margin: 0;
        overflow: visible;
        text-align: left;
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