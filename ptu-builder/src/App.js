import { Route, Switch, Redirect } from "react-router-dom";

import Welcome from "./pages/Welcome";
import MainHeader from "./components/MainHeader";
import Builder from "./pages/Builder"

const App = () => {

  return <div>
  <MainHeader/>
  <main>
    <Switch>
  <Route path="/" exact>
    <Redirect to="/welcome"/>
  </Route>
  <Route path="/welcome">
    <Welcome/>
  </Route>
  <Route path="/builder" exact>
        <Builder />
  </Route>
  </Switch></main>
</div>;
};

export default App;
