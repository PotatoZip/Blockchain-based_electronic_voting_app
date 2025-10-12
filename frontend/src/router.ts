import { createRouter, createWebHistory } from "vue-router";
import Home from "./pages/Home.vue";
import Votings from "./pages/Votings.vue";
import About from "./pages/About.vue";
import Verify from "./pages/Verify.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Home },
    { path: "/elections", component: Votings },
    { path: "/about", component: About },
    { path: "/elections/:id/verify", component: Verify },
  ],
});
