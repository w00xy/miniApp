import { createRouter, createWebHistory } from 'vue-router'
import TasksView from '../views/TasksView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Tasks',
      component: TasksView,
    },
    {
      path: '/profile',
      name: 'Profile',
      component: ProfileView,
    },
  ],
})

export default router
