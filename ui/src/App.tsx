import { Route, Routes, NavLink } from "react-router-dom";
import JobsPage from "./pages/JobsPage";
import RunDetailPage from "./pages/RunDetailPage";

const App = () => {
  return (
    <div className="layout">
      <header>
        <nav className="grid two">
          <NavLink to="/" end>
            Jobs
          </NavLink>
          <NavLink to="/runs">Runs</NavLink>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<JobsPage />} />
          <Route path="/runs" element={<RunDetailPage />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;

