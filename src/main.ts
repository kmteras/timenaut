import Vue from 'vue'
import App from './app.vue'
import 'material-design-icons/iconfont/material-icons.css'
import 'bulma/css/bulma.css'

Vue.config.productionTip = false;

new Vue({
    render: h => h(App),
}).$mount('#app');
