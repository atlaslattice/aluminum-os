import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Home from "./pages/Home";
import Lattice from "./pages/Lattice";
import Elements from "./pages/Elements";
import Routing from "./pages/Routing";
import Governance from "./pages/Governance";
import Strategy from "./pages/Strategy";
import Mirror from "./pages/Mirror";
import Appendix from "./pages/Appendix";
import Market from "./pages/Market";
import Dashboard from "./pages/Dashboard";
import Ingestion from "./pages/Ingestion";
import Layers from "./pages/Layers";
import Glossary from "./pages/Glossary";
import Sovereignty from "./pages/Sovereignty";
import DialectsPage from "./pages/Dialects";
import ComputeZones from "./pages/ComputeZones";
import AntiMonoculture from "./pages/AntiMonoculture";
import ProvenancePage from "./pages/Provenance";
import SimulationPage from "./pages/Simulation";
import Invariants from "./pages/Invariants";
import Doctrines from "./pages/Doctrines";
import Verifier from "./pages/Verifier";
import Canon from "./pages/Canon";
function Router() {
  // make sure to consider if you need authentication for certain routes
  return (
    <Switch>
      <Route path={"/"} component={Home} />
      <Route path={"/lattice"} component={Lattice} />
      <Route path={"/elements"} component={Elements} />
      <Route path={"/routing"} component={Routing} />
      <Route path={"/governance"} component={Governance} />
      <Route path={"/strategy"} component={Strategy} />
      <Route path={"/mirror"} component={Mirror} />
      <Route path={"/market"} component={Market} />
      <Route path={"/dashboard"} component={Dashboard} />
      <Route path={"/appendix"} component={Appendix} />
      <Route path={"/ingestion"} component={Ingestion} />
      <Route path={"/layers"} component={Layers} />
      <Route path={"/glossary"} component={Glossary} />
      <Route path={"/sovereignty"} component={Sovereignty} />
      <Route path={"/dialects"} component={DialectsPage} />
      <Route path={"/compute-zones"} component={ComputeZones} />
      <Route path={"/anti-monoculture"} component={AntiMonoculture} />
      <Route path={"/provenance"} component={ProvenancePage} />
      <Route path={"/simulation"} component={SimulationPage} />
      <Route path={"/invariants"} component={Invariants} />
      <Route path={"/doctrines"} component={Doctrines} />
      <Route path={"/verifier"} component={Verifier} />
      <Route path={"/canon"} component={Canon} />
      <Route path={"/404"} component={NotFound} />
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="dark">
        <TooltipProvider>
          <Toaster />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
