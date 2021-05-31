import React from "react";
import "./App.css";
import Encrypt from "./Pages/Encrypt";
import Decrypt from "./Pages/Decrypt";
import { Switch, Route, HashRouter } from "react-router-dom";

const App = () => ( 
  <HashRouter basename="/">
    <Switch> 
      <Route path="/" exact component={Encrypt} />
      <Route path="/decrypt" exact component={Decrypt} />
    </Switch>
  </HashRouter>
);

export default App;
