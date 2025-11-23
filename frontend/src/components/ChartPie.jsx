import React from "react";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Title,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend, Title);

const ChartPie = ({ data }) => {
  if (!data || Object.keys(data).length === 0)
    return <p>No data available for Pie Chart</p>;

  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        data: Object.values(data),
        backgroundColor: [
          "#4e79a7",
          "#f28e2b",
          "#e15759",
          "#76b7b2",
          "#59a14f",
          "#edc949",
        ],
      },
    ],
  };

  return (
    <div style={{ width: "350px" }}>
      <h4>Equipment Type Distribution</h4>
      <Pie data={chartData} />
    </div>
  );
};

export default ChartPie;
