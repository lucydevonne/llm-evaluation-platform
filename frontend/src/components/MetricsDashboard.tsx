import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { ModelPerformance } from '../types/types';

interface MetricsDashboardProps {
  modelPerformance: ModelPerformance;
}

const MetricsDashboard: React.FC<MetricsDashboardProps> = ({ modelPerformance }) => {
  // Transform the data for the chart
  const chartData = Object.entries(modelPerformance).map(([model, metrics]) => ({
    name: model,
    responseTime: metrics.avgResponseTime,
    accuracy: metrics.avgAccuracy,
    relevancy: metrics.avgRelevancy
  }));

  // Don't render if there's no data
  if (chartData.length === 0) {
    return null;
  }

  return (
    <div>
      <h2>Model Performance Metrics</h2>
      <div style={{ width: '100%', height: 300, marginTop: '20px' }}>
        <BarChart
          width={600}
          height={300}
          data={chartData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="responseTime" fill="#8884d8" name="Response Time (ms)" />
          <Bar dataKey="accuracy" fill="#82ca9d" name="Accuracy Score" />
          <Bar dataKey="relevancy" fill="#ffc658" name="Relevancy Score" />
        </BarChart>
      </div>
    </div>
  );
};

export default MetricsDashboard;