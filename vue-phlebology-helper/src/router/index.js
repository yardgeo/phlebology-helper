import Vue from 'vue'
import VueRouter from 'vue-router'
import functions from "./functions";
import routes from "./routes";

Vue.use(VueRouter);

const router = new VueRouter({
  routes,
  mode: 'history',
});


router.beforeEach((to, from, next) => {
  functions.updatePageTitleAndMeta(document, to, next);
  functions.handleUnauthorizedAccess(to, next);
});

export default router
