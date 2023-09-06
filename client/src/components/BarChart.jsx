import { useState, useEffect } from "react";
import settings from "../config/settings.json";
import axios from "axios";
import { Chart } from "react-google-charts";

const BarChart = () => {
  const [barChartAcoustics, setBarChartAcoustics] = useState([
    ["Songs", "Acousticness"],
  ]);
  const [barChartTempo, setBarChartTempo] = useState([["Songs", "Tempo"]]);

  useEffect(() => {
    async function fetchBarChartData() {
      const { data } = await axios.get(`${settings.apiUrl}/songs/barChart`);

      data.acoustics.unshift(["Songs", "Acousticness"]);
      data.tempo.unshift(["Songs", "Tempo"]);

      setBarChartAcoustics(data.acoustics);
      setBarChartTempo(data.tempo);
    }
    fetchBarChartData();
  }, []);

  return (
    <>
      <div data-testid="mock-bar-chart-1">
        <Chart
          chartType="Bar"
          width="100%"
          height="500px"
          data={barChartAcoustics}
          options={{
            chart: {
              title: "Acoustics of Songs",
            },
            colors: ["#dc3912"],
            legend: { position: "none" },
          }}
        />
      </div>
      <div data-testid="mock-bar-chart-2">
        <Chart
          chartType="Bar"
          width="100%"
          height="500px"
          data={barChartTempo}
          options={{
            chart: {
              title: "Tempo of Songs",
            },
            colors: ["#3366cc"],
            legend: { position: "none" },
          }}
        />
      </div>
    </>
  );
};

export default BarChart;
