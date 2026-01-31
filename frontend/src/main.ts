import { createApp } from 'vue'
import App from './App.vue'

import router from './router'
import './assets/tailwind.css'

import '@fontsource/roboto/300.css'
import '@fontsource/roboto/400.css'
import '@fontsource/roboto/700.css'

createApp(App).use(router).mount('#app')
