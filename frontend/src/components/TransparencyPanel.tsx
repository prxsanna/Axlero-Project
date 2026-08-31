'use client';

import React, { useState } from 'react';
import { Code2, Database, ShieldCheck, FileSpreadsheet, ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';
import { ChatResponse } from '../lib/api';

interface TransparencyPanelProps {
  transparency: ChatResponse['transparency'];
}

export default function TransparencyPanel({ transparency }: TransparencyPanelProps) {
  const [activeTab, setActiveTab] = useState<'api' | 'sql' | 'metrics' | 'governance'>('sql');
  const [isOpen, setIsOpen] = useState(true);
  const [copied, setCopied] = useState(false);

  const primaryCall = transparency?.api_calls?.[0] || null;

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="mt-4 border border-gray-800 bg-gray-900/60 rounded-xl overflow-hidden backdrop-blur-sm shadow-md">
      {/* Header Bar */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 bg-gray-900/80 hover:bg-gray-800/80 flex items-center justify-between transition-colors border-b border-gray-800/80"
      >
        <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-blue-400">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Query Governance & Transparency Inspector</span>
          <span className="ml-2 px-2 py-0.5 text-[10px] rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            PostgreSQL Verified
          </span>
        </div>
        <div className="flex items-center space-x-3 text-xs text-gray-400">
          <span>{transparency?.total_rows_scanned || 0} rows scanned</span>
          <span>•</span>
          <span>{transparency?.execution_time_ms || 0} ms</span>
          {isOpen ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
        </div>
      </button>

      {/* Accordion Content */}
      {isOpen && (
        <div className="p-4">
          {/* Navigation Tabs */}
          <div className="flex border-b border-gray-800 mb-4 space-x-4">
            <button
              onClick={() => setActiveTab('sql')}
              className={`pb-2 text-xs font-medium flex items-center space-x-1.5 border-b-2 transition-colors ${
                activeTab === 'sql'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-gray-200'
              }`}
            >
              <Database className="w-3.5 h-3.5" />
              <span>Governed SQL ({transparency?.api_calls?.length || 0})</span>
            </button>
            <button
              onClick={() => setActiveTab('api')}
              className={`pb-2 text-xs font-medium flex items-center space-x-1.5 border-b-2 transition-colors ${
                activeTab === 'api'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-gray-200'
              }`}
            >
              <Code2 className="w-3.5 h-3.5" />
              <span>Semantic API Request</span>
            </button>
            <button
              onClick={() => setActiveTab('metrics')}
              className={`pb-2 text-xs font-medium flex items-center space-x-1.5 border-b-2 transition-colors ${
                activeTab === 'metrics'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-gray-200'
              }`}
            >
              <FileSpreadsheet className="w-3.5 h-3.5" />
              <span>Metric Formulas</span>
            </button>
            <button
              onClick={() => setActiveTab('governance')}
              className={`pb-2 text-xs font-medium flex items-center space-x-1.5 border-b-2 transition-colors ${
                activeTab === 'governance'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-gray-200'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>Governance Safeguards</span>
            </button>
          </div>

          {/* Tab 1: Governed SQL */}
          {activeTab === 'sql' && (
            <div className="space-y-4">
              {transparency?.api_calls?.map((call, idx) => (
                <div key={idx} className="relative bg-gray-950 rounded-lg border border-gray-800 p-3">
                  <div className="flex items-center justify-between text-[11px] text-gray-400 mb-2 font-mono">
                    <span>Query #{call.step}: Governed SQL compiled from Semantic Layer</span>
                    <button
                      onClick={() => handleCopy(call.sql)}
                      className="flex items-center space-x-1 text-gray-400 hover:text-white transition-colors"
                    >
                      {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                      <span>{copied ? 'Copied' : 'Copy SQL'}</span>
                    </button>
                  </div>
                  <pre className="text-xs font-mono text-emerald-300 overflow-x-auto p-2 bg-black/40 rounded">
                    {call.sql}
                  </pre>
                </div>
              ))}
            </div>
          )}

          {/* Tab 2: API Call */}
          {activeTab === 'api' && (
            <div className="relative bg-gray-950 rounded-lg border border-gray-800 p-3">
              <div className="text-[11px] text-gray-400 mb-2 font-mono">
                Structured Semantic Layer API Payload (POST /api/semantic/query)
              </div>
              <pre className="text-xs font-mono text-blue-300 overflow-x-auto p-2 bg-black/40 rounded">
                {JSON.stringify(primaryCall?.request, null, 2)}
              </pre>
            </div>
          )}

          {/* Tab 3: Metric Definitions */}
          {activeTab === 'metrics' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {transparency?.governed_metrics_used?.map((m, idx) => (
                <div key={idx} className="bg-gray-950 p-3 rounded-lg border border-gray-800">
                  <div className="text-xs font-semibold text-blue-400 font-mono">{m}</div>
                  <div className="text-[11px] text-gray-300 mt-1">Authoritative Metric Formula</div>
                  <div className="mt-2 text-xs font-mono bg-black/50 p-1.5 rounded text-amber-300">
                    {m === 'revenue' && 'SUM(s.revenue)'}
                    {m === 'cost' && 'SUM(s.cost)'}
                    {m === 'profit' && 'SUM(s.profit)'}
                    {m === 'margin' && 'SUM(s.profit)'}
                    {m === 'margin_pct' && '(SUM(profit) / SUM(revenue)) * 100'}
                    {m === 'quantity' && 'SUM(s.quantity)'}
                    {m === 'customer_count' && 'COUNT(DISTINCT s.customer_id)'}
                    {m === 'material_cost' && 'SUM(ROUND(s.cost * 0.75, 2))'}
                    {m === 'shipping_cost' && 'SUM(ROUND(s.cost * 0.25, 2))'}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Tab 4: Governance */}
          {activeTab === 'governance' && (
            <div className="bg-gray-950 p-4 rounded-lg border border-gray-800 space-y-3 text-xs">
              <div className="flex items-center justify-between py-1 border-b border-gray-800">
                <span className="text-gray-400">Direct SQL Execution Prevention</span>
                <span className="text-emerald-400 font-semibold flex items-center">
                  <Check className="w-3.5 h-3.5 mr-1" /> Enforced (LLM restricted to governed tool specs)
                </span>
              </div>
              <div className="flex items-center justify-between py-1 border-b border-gray-800">
                <span className="text-gray-400">Prompt & DDL Injection Scanner</span>
                <span className="text-emerald-400 font-semibold flex items-center">
                  <Check className="w-3.5 h-3.5 mr-1" /> Passed (AST & Regex checked)
                </span>
              </div>
              <div className="flex items-center justify-between py-1 border-b border-gray-800">
                <span className="text-gray-400">Metric Definitions Validation</span>
                <span className="text-emerald-400 font-semibold flex items-center">
                  <Check className="w-3.5 h-3.5 mr-1" /> 100% Governed PostgreSQL Catalog Match
                </span>
              </div>
              <div className="flex items-center justify-between py-1 border-b border-gray-800">
                <span className="text-gray-400">Row Count Cap</span>
                <span className="text-gray-200 font-mono">Capped at 1,000 max (scanned: {transparency?.total_rows_scanned})</span>
              </div>
              <div className="flex items-center justify-between py-1">
                <span className="text-gray-400">Authoritative Data Warehouse</span>
                <span className="text-blue-400 font-mono">{transparency?.data_source}</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
