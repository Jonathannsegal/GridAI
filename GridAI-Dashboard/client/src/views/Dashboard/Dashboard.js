import React from "react";

// @material-ui/core
import { makeStyles } from "@material-ui/core/styles";
import styles from "assets/jss/material-dashboard-react/views/dashboardStyle.js";
import GraphDisplay from "components/GraphDisplay/graphdisplay.js"
import { Grid } from "@material-ui/core";

const useStyles = makeStyles(styles);

export default function Dashboard() {
  const classes = useStyles();
  return (
    <div>
      <GraphDisplay />
    </div>
  );
}
