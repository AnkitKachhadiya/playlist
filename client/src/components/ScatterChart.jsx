import { useState, useEffect } from "react";
import settings from "../config/settings.json";
import axios from "axios";
import { Chart } from "react-google-charts";

const ScatterChart = () => {
  const [scatterChart, setScatterChart] = useState([]);

  useEffect(() => {
    async function fetchScatterChartData() {
      const { data } = await axios.get(`${settings.apiUrl}/songs/scatterChart`);

      data.unshift(["Songs", "Danceability"]);

      setScatterChart(data);
    }
    fetchScatterChartData();
  }, []);

  return (
    <div data-testid="mock-scatter-chart">
      <Chart
        chartType="ScatterChart"
        width="100%"
        height="700px"
        data={scatterChart}
        options={{
          title: "Song Danceability",
          curveType: "function",
          legend: { position: "bottom" },
        }}
      />
    </div>
  );
};

export default ScatterChart;
