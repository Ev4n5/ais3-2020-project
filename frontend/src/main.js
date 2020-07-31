import Vue from 'vue'
import App from './App.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faCalendarAlt } from '@fortawesome/free-regular-svg-icons'
import { faCaretDown, faCircle } from '@fortawesome/free-solid-svg-icons'

library.add(faCalendarAlt)
library.add(faCaretDown)
library.add(faCircle)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
