# frontend/src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import AboutView from '../views/AboutView.vue';
import LoginForm from '../components/LoginForm.vue';
import Dashboard from '../components/Dashboard.vue';
import NotesComponent from '../components/NotesComponent.vue';
import ToDoComponent from '../components/ToDoComponent.vue';
import EmailComponent from '../components/EmailComponent.vue';
import JIRAComponent from '../components/JIRAComponent.vue';
import RealTimeComponent from '../components/RealTimeComponent.vue';
import SocialMediaComponent from '../components/SocialMediaComponent.vue'
import SmartHomeComponent from '../components/SmartHomeComponent.vue'
import TravelComponent from '../components/TravelComponent.vue';
import PlanView from '../components/PlanView.vue';
import ReportsComponent from '../components/ReportsComponent.vue';
import SettingsComponent from '../components/SettingsComponent.vue';
import { useUserStore } from '../stores/userStore';
import { computed } from 'vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginForm
    },
      {
          path: '/dashboard',
          component: Dashboard,
        meta: { requiresAuth: true },
          children: [
              {
                  path: 'notes',
                  component: NotesComponent
              },
               {
                  path: 'todos',
                  component: ToDoComponent
                },
                {
                  path: 'email',
                    component: EmailComponent
                },
                {
                    path: 'jira',
                    component: JIRAComponent
                },
              {
                path: 'realtime',
                component: RealTimeComponent
              },
              {
                  path: 'social_media',
                  component: SocialMediaComponent
                },
              {
                  path: 'smart_home',
                  component: SmartHomeComponent
              },
              {
                path: 'travel',
                component: TravelComponent
                },
              {
                  path: 'plan',
                  component: PlanView
                },
              {
                  path: 'reports',
                  component: ReportsComponent
              },
              {
                path: 'settings',
                component: SettingsComponent
              }
          ]
      }
  ]
});
router.beforeEach((to) => {
    const userStore = useUserStore();
    const isLoggedIn = computed(() => userStore.isLoggedIn);
    if (to.meta.requiresAuth && !isLoggedIn.value) {
        return '/login'
    }
});
export default router;