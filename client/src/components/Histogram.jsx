import { useState, useEffect } from "react";
import settings from "../config/settings.json";
import axios from "axios";
import { Chart } from "react-google-charts";

const Histogram = () => {
  const [histogram, setHistogram] = useState([["Song", "Duration in seconds"]]);

  useEffect(() => {
    async function fetchHistogramData() {
      const { data } = await axios.get(`${settings.apiUrl}/songs/histogram`);

      data.unshift(["Song", "Duration in seconds"]);

      setHistogram(data);
    }
    fetchHistogramData();
  }, []);

  return (
    <div data-testid="mock-histogram">
      <Chart
        chartType="Histogram"
        data={histogram}
        width="100%"
        height="700px"
        options={{
          title: "Duration of songs in seconds",
          legend: { position: "none" },
        }}
      />
    </div>
  );
};

export default Histogram;
