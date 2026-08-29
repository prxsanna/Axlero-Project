'use client';

import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';

interface DynamicChartProps {
  option: any;
  height?: string;
}

export default function DynamicChart({ option, height = '350px' }: DynamicChartProps) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted || !option) {
    return (
      <div 
        style={{ height }} 
        className="w-full bg-dark-card border border-dark-border rounded-xl flex items-center justify-center text-gray-500 animate-pulse"
      >
        <span>Loading chart visualization...</span>
      </div>
    );
  }

  return (
    <div className="w-full bg-dark-card border border-dark-border rounded-xl p-4 shadow-lg">
      <ReactECharts
        option={option}
        style={{ height, width: '100%' }}
        opts={{ renderer: 'canvas' }}
      />
    </div>
  );
}
