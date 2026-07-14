import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/posts',
      name: 'post-list',
      component: () => import('../views/PostListView.vue')
    },
    {
      path: '/posts/:id',
      name: 'post-detail',
      component: () => import('../views/PostDetailView.vue')
    },
    {
      path: '/posts/write',
      name: 'post-write',
      component: () => import('../views/PostFormView.vue')
    },
    {
      path: '/posts/:id/edit',
      name: 'post-edit',
      component: () => import('../views/PostFormView.vue')
    }
  ]
})

export default router