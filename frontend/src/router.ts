import { createRouter, createWebHistory } from "vue-router";
import Home from "./pages/Home.vue";
import Votings from "./pages/Votings.vue";
import About from "./pages/About.vue";
import Verify from "./pages/Verify.vue";
import Vote from "./pages/Vote.vue";
import Results from "./pages/Results.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Home },
    { path: "/elections", component: Votings },
    { path: "/about", component: About },
    { path: "/elections/:id/verify", component: Verify },
    { path: "/elections/:id/vote", component: Vote },
    { path: "/elections/:id/results", component: Results },
  ],
});
