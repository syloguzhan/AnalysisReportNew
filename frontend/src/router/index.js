import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import HistoryView from "../views/HistoryView.vue";
import ReportView from "../views/ReportView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "input",
    component: HomeView,
  },
  {
    path: "/history",
    name: "history",
    component: HistoryView,
  },
  {
    path: '/report/:domain',
    name: 'Report',
    component: ReportView,
    props: true
  }
];

const router = new VueRouter({
  routes,
});

export default router;
