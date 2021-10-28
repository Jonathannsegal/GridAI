/*!

=========================================================
* Material Dashboard React - v1.9.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/material-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
// @material-ui/icons
import Dashboard from "@material-ui/icons/Dashboard";
// core components/views for Admin layout
import DashboardPage from "views/Dashboard/Dashboard.js";
import AnomalyPage from "views/TablePage/AnomalyPage.js"
import NodeInfo from "views/Dashboard/NodeInfo";

const dashboardRoutes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    rtlName: "لوحة القيادة",
    icon: Dashboard,
    component: DashboardPage,
    layout: "/admin"
  },
  {
    path: "/anomaly",
    name: "Anomaly Table",
    rtlName: "قائمة الجدول",
    icon: "content_paste",
    component: AnomalyPage,
    layout: "/admin"
  },
  {
    path: "/nodeinfo",
    name: "Node Info",
    icon: "content_paste",
    component: NodeInfo,
    layout: "/admin"
  }
];

export default dashboardRoutes;
