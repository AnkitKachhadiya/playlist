import { expect, test } from "vitest";
import { render } from "@testing-library/react";
import { StaticRouter } from "react-router-dom/server";
import BarChart from "../components/BarChart";
import ScatterChart from "../components/ScatterChart";
import Histogram from "../components/Histogram";

test("displays a acoustics and tempo bar charts", async () => {
  const { findByTestId } = render(
    <StaticRouter>
      <BarChart />
    </StaticRouter>,
  );

  expect(findByTestId("mock-bar-chart-1")).toBeDefined();
  expect(findByTestId("mock-bar-chart-2")).toBeDefined();
});

test("displays a scatter chart", async () => {
  const { findByTestId } = render(
    <StaticRouter>
      <ScatterChart />
    </StaticRouter>,
  );

  expect(findByTestId("mock-scatter-chart")).toBeDefined();
});

test("displays a histogram", async () => {
  const { findByTestId } = render(
    <StaticRouter>
      <Histogram />
    </StaticRouter>,
  );

  expect(findByTestId("mock-histogram")).toBeDefined();
});
