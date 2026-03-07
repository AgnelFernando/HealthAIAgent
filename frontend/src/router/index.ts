import { createRouter, createWebHashHistory } from 'vue-router'

import ChatView from '../views/ChatView.vue'
import DashboardView from '../views/DashboardView.vue'
import ProfileView from '../views/ProfileView.vue'
import HistoryView from '../views/HistoryView.vue'

const routes = [
  { path: '/', component: ChatView },
  { path: '/dashboard', component: DashboardView },
  { path: '/profile', component: ProfileView },
  { path: '/history', component: HistoryView },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
