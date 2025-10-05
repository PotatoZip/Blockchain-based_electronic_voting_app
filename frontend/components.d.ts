export {};

declare module "vue" {
  export interface GlobalComponents {
    IHeroiconsOutlineHome: typeof import("~icons/heroicons-outline/home")["default"];
    IMdiAccount: typeof import("~icons/mdi/account")["default"];
    Navbar: typeof import("./src/components/Navbar.vue")["default"];
    QuestionsList: typeof import("./src/components/QuestionsList.vue")["default"];
    RouterLink: typeof import("vue-router")["RouterLink"];
    RouterView: typeof import("vue-router")["RouterView"];
  }
}
