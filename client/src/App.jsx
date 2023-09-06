import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes, Link } from "react-router-dom";
import Table from "./components/Table";
import ScatterChart from "./components/ScatterChart";
import BarChart from "./components/BarChart";
import Histogram from "./components/Histogram";
import { AppBar, Toolbar, Typography } from "@mui/material";

const App = () => {
  return (
    <BrowserRouter>
      <div className="nav-bar-wrapper">
        <AppBar>
          <Toolbar className="nav-bar">
            <Typography>
              <Link to="/" className="nav-link">
                Home
              </Link>
            </Typography>
            <Typography>
              <Link to="/scatter-chart" className="nav-link">
                Scatter Chart
              </Link>
            </Typography>
            <Typography>
              <Link to="/histogram" className="nav-link">
                Histogram
              </Link>
            </Typography>
            <Typography>
              <Link to="/bar-chart" className="nav-link">
                Bar Chart
              </Link>
            </Typography>
          </Toolbar>
        </AppBar>
      </div>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Table />
            </>
          }
        />
        <Route
          path="/scatter-chart"
          element={
            <>
              <ScatterChart />
            </>
          }
        />
        <Route
          path="/histogram"
          element={
            <>
              <Histogram />
            </>
          }
        />
        <Route
          path="/bar-chart"
          element={
            <>
              <BarChart />
            </>
          }
        />
        <Route path="/show" element="show" />
      </Routes>
    </BrowserRouter>
  );
};

const container = document.getElementById("root");

if (!container) {
  throw new Error("Couldn't find root element");
}

const root = createRoot(container);
root.render(<App />);
