import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

if (window.Telegram.WebApp) {
    window.Telegram.WebApp.ready()
    window.Telegram.WebApp.expand()
}

app.use(router)

app.mount('#app')

