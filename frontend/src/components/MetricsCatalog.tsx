'use client';

import React, { useEffect, useState } from 'react';
import { Database, Calculator, ChevronRight, Sparkles } from 'lucide-react';
import { fetchMetricsCatalog, MetricsCatalogResponse } from '../lib/api';

interface MetricsCatalogProps {
  onSelectQuery?: (sampleQuery: string) => void;
}

export default function MetricsCatalog({ onSelectQuery }: MetricsCatalogProps) {
  const [catalog, setCatalog] = useState<MetricsCatalogResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'measures' | 'dimensions'>('measures');

  useEffect(() => {
    fetchMetricsCatalog()
      .then(setCatalog)
      .catch((err) => console.error('Failed to load metrics catalog:', err));
  }, []);

  return (
    <aside className="w-80 bg-gray-900 border-r border-gray-800 flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-gray-800 flex items-center space-x-2">
        <Database className="w-5 h-5 text-blue-400" />
        <div>
          <h2 className="font-semibold text-sm text-gray-100">Governed Semantic Layer</h2>
          <p className="text-[11px] text-gray-400">PostgreSQL Metric & Dimension Catalog</p>
        </div>
      </div>

      {/* Mode Switcher */}
      <div className="p-3 border-b border-gray-800 bg-gray-950/40">
        <div className="flex bg-gray-900 p-1 rounded-lg border border-gray-800">
          <button
            onClick={() => setActiveTab('measures')}
            className={`flex-1 py-1.5 text-xs font-medium rounded-md transition-colors ${
              activeTab === 'measures'
                ? 'bg-blue-600 text-white shadow'
                : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            Measures ({catalog ? Object.keys(catalog.measures).length : 0})
          </button>
          <button
            onClick={() => setActiveTab('dimensions')}
            className={`flex-1 py-1.5 text-xs font-medium rounded-md transition-colors ${
              activeTab === 'dimensions'
                ? 'bg-blue-600 text-white shadow'
                : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            Dimensions ({catalog ? Object.keys(catalog.dimensions).length : 0})
          </button>
        </div>
      </div>

      {/* List Content */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {activeTab === 'measures' && catalog && (
          Object.entries(catalog.measures).map(([key, item]) => (
            <div
              key={key}
              className="p-3 bg-gray-950 rounded-xl border border-gray-800/80 hover:border-blue-500/50 transition-all group"
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-semibold text-blue-400">{item.name}</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-300 font-mono">
                  {item.unit}
                </span>
              </div>
              <p className="text-xs font-medium text-gray-200 mt-1">{item.label}</p>
              <p className="text-[11px] text-gray-400 mt-0.5">{item.description}</p>
              <div className="mt-2 pt-2 border-t border-gray-800/60 flex items-center text-[10px] text-amber-400 font-mono bg-black/40 px-2 py-1 rounded">
                <Calculator className="w-3 h-3 mr-1 text-amber-500 shrink-0" />
                <span className="truncate">{item.sql_formula}</span>
              </div>
            </div>
          ))
        )}

        {activeTab === 'dimensions' && catalog && (
          Object.entries(catalog.dimensions).map(([key, item]) => (
            <div
              key={key}
              className="p-3 bg-gray-950 rounded-xl border border-gray-800/80 hover:border-emerald-500/50 transition-all"
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-semibold text-emerald-400">{item.name}</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-300 font-mono uppercase">
                  {item.type}
                </span>
              </div>
              <p className="text-xs font-medium text-gray-200 mt-1">{item.label}</p>
              <div className="mt-1 text-[10px] text-gray-400 font-mono">
                Source Column: <span className="text-gray-300">{item.sql_column}</span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Suggested Demo Scenario Card */}
      <div className="p-3 border-t border-gray-800 bg-gray-950">
        <div className="p-3 bg-gradient-to-br from-blue-900/30 to-purple-900/20 border border-blue-500/30 rounded-xl">
          <div className="flex items-center space-x-1.5 text-xs font-semibold text-blue-300 mb-1">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            <span>Multi-Step Demo Question</span>
          </div>
          <button
            onClick={() => onSelectQuery && onSelectQuery("Why did our European margins drop last quarter?")}
            className="w-full text-left text-xs text-gray-300 hover:text-white bg-blue-500/10 hover:bg-blue-500/20 p-2 rounded-lg border border-blue-500/20 transition-all flex items-center justify-between group mt-2"
          >
            <span className="line-clamp-2 italic">"Why did our European margins drop last quarter?"</span>
            <ChevronRight className="w-4 h-4 text-blue-400 group-hover:translate-x-0.5 transition-transform shrink-0" />
          </button>
        </div>
      </div>
    </aside>
  );
}
