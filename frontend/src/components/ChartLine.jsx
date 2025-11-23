import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const ChartLine = ({ summary }) => {
  if (!summary) return <p>No summary data available</p>;

  const chartData = {
    labels: ["Flowrate", "Pressure", "Temperature"],
    datasets: [
      {
        label: "Average Values",
        data: [
          summary.average_flowrate,
          summary.average_pressure,
          summary.average_temperature,
        ],
        backgroundColor: "#4e79a7",
      },
    ],
  };

  return (
    <div style={{ width: "350px" }}>
      <h4>Average Parameter Values</h4>
      <Bar data={chartData} />
    </div>
  );
};

export default ChartLine;
