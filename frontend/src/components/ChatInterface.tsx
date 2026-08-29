'use client';

import React, { useState } from 'react';
import { Send, Bot, User, Sparkles, AlertTriangle, CheckCircle2, ChevronRight, RefreshCw, BarChart2, Shield } from 'lucide-react';
import { ChatResponse, sendChatMessage } from '../lib/api';
import DynamicChart from './DynamicChart';
import TransparencyPanel from './TransparencyPanel';

interface ChatInterfaceProps {
  externalPrompt?: string;
  onClearPrompt?: () => void;
}

export default function ChatInterface({ externalPrompt, onClearPrompt }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Array<{
    id: string;
    role: 'user' | 'assistant';
    content: string;
    responseObject?: ChatResponse;
    error?: string;
  }>>([
    {
      id: 'welcome',
      role: 'assistant',
      content: "Hello! I am **MetricMind**, your Conversational BI Agent. Ask any natural language question to explore governed metrics, compare regional performance, or run multi-step root-cause analysis backed by PostgreSQL."
    }
  ]);

  const [inputPrompt, setInputPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [expandedSteps, setExpandedSteps] = useState<Record<string, boolean>>({});

  React.useEffect(() => {
    if (externalPrompt) {
      handleSend(externalPrompt);
      if (onClearPrompt) onClearPrompt();
    }
  }, [externalPrompt]);

  const handleSend = async (promptToSend?: string) => {
    const queryText = promptToSend || inputPrompt;
    if (!queryText.trim() || loading) return;

    const userMsgId = Date.now().toString();
    const userMessage = { id: userMsgId, role: 'user' as const, content: queryText };

    setMessages((prev) => [...prev, userMessage]);
    if (!promptToSend) setInputPrompt('');
    setLoading(true);

    try {
      const result = await sendChatMessage(queryText);
      const assistantMsgId = (Date.now() + 1).toString();

      setMessages((prev) => [
        ...prev,
        {
          id: assistantMsgId,
          role: 'assistant',
          content: result.explanation,
          responseObject: result
        }
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: "An error occurred while executing governed semantic query.",
          error: err.message || "Failed to complete agent query."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const toggleSteps = (msgId: string) => {
    setExpandedSteps((prev) => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-dark-base overflow-hidden">
      {/* Top Bar Header */}
      <header className="h-14 border-b border-gray-800 bg-gray-900/60 px-6 flex items-center justify-between backdrop-blur-md">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center">
            <Bot className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <h1 className="font-semibold text-sm text-gray-100 flex items-center space-x-2">
              <span>MetricMind BI Workspace</span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                PostgreSQL + Cube.dev + LangChain + Gemini
              </span>
            </h1>
            <p className="text-[11px] text-gray-400">Next.js • LangChain Agent • dbt Mart • PostgreSQL (50k sales)</p>
          </div>
        </div>

        {/* Governance Status Pill */}
        <div className="hidden md:flex items-center space-x-2 bg-gray-950 px-3 py-1.5 rounded-full border border-gray-800 text-xs text-gray-300">
          <Shield className="w-4 h-4 text-emerald-400" />
          <span>LLM Injection Protected</span>
        </div>
      </header>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex space-x-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/40 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 text-blue-400" />
              </div>
            )}

            <div className={`max-w-3xl rounded-2xl p-5 shadow-lg ${
              msg.role === 'user'
                ? 'bg-blue-600 text-white rounded-tr-none'
                : 'bg-dark-card border border-dark-border text-gray-200 rounded-tl-none w-full'
            }`}>
              {/* Message Header */}
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider text-gray-400">
                  {msg.role === 'user' ? 'Business User Prompt' : 'Governed Analytical Response'}
                </span>
                {msg.responseObject && (
                  <span className="text-[10px] text-emerald-400 font-mono flex items-center">
                    <CheckCircle2 className="w-3 h-3 mr-1" /> PostgreSQL Governed Result
                  </span>
                )}
              </div>

              {/* Error Alert */}
              {msg.error && (
                <div className="p-3 bg-red-950/60 border border-red-800 text-red-200 rounded-lg text-xs flex items-center space-x-2 my-2">
                  <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
                  <span>{msg.error}</span>
                </div>
              )}

              {/* Multi-Step Agent Reasoning Trace Toggle */}
              {msg.responseObject?.reasoning_steps && (
                <div className="my-3 border border-blue-500/20 bg-blue-950/30 rounded-xl overflow-hidden">
                  <button
                    onClick={() => toggleSteps(msg.id)}
                    className="w-full px-4 py-2.5 bg-blue-900/20 hover:bg-blue-900/40 flex items-center justify-between text-xs font-medium text-blue-300 transition-colors"
                  >
                    <div className="flex items-center space-x-2">
                      <Sparkles className="w-4 h-4 text-blue-400" />
                      <span>Multi-Step Agent Reasoning Trace ({msg.responseObject.reasoning_steps.length} Steps)</span>
                    </div>
                    <ChevronRight className={`w-4 h-4 transition-transform ${expandedSteps[msg.id] ? 'rotate-90' : ''}`} />
                  </button>

                  {expandedSteps[msg.id] && (
                    <div className="p-4 space-y-3 bg-gray-950/80 border-t border-blue-500/20 font-mono text-xs">
                      {msg.responseObject.reasoning_steps.map((step, sIdx) => (
                        <div key={sIdx} className="pl-3 border-l-2 border-blue-500 space-y-1">
                          <div className="text-blue-400 font-semibold">Step {step.step}: {step.action}</div>
                          {step.thought && <div className="text-gray-300 italic">Thought: {step.thought}</div>}
                          {step.generated_sql && (
                            <div className="text-emerald-300 bg-black/60 p-2 rounded text-[11px] whitespace-pre-wrap">
                              {step.generated_sql}
                            </div>
                          )}
                          {step.observation && <div className="text-amber-300">Observation: {step.observation}</div>}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Main Content */}
              <div className="prose prose-invert prose-sm max-w-none space-y-2 leading-relaxed whitespace-pre-wrap">
                {msg.content}
              </div>

              {/* ECharts Visualization */}
              {msg.responseObject?.chart_config && (
                <div className="mt-5">
                  <DynamicChart option={msg.responseObject.chart_config} height="360px" />
                </div>
              )}

              {/* Transparency Panel */}
              {msg.responseObject?.transparency && (
                <TransparencyPanel transparency={msg.responseObject.transparency} />
              )}
            </div>
          </div>
        ))}

        {/* Loading Spinner */}
        {loading && (
          <div className="flex space-x-4">
            <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/40 flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4 text-blue-400 animate-spin" />
            </div>
            <div className="bg-dark-card border border-dark-border p-4 rounded-2xl text-xs text-gray-300 flex items-center space-x-3">
              <RefreshCw className="w-4 h-4 text-blue-400 animate-spin" />
              <span>Analyzing intent via Gemini, orchestrating LangChain tools, and querying PostgreSQL...</span>
            </div>
          </div>
        )}
      </div>

      {/* Sample Quick Action Pills */}
      <div className="px-6 py-2 border-t border-gray-800 bg-gray-950 flex flex-wrap gap-2">
        <button
          onClick={() => handleSend("How much revenue did we make in Europe?")}
          className="text-xs bg-gray-900 hover:bg-gray-800 text-gray-300 border border-gray-800 px-3 py-1.5 rounded-full transition-colors flex items-center space-x-1.5"
        >
          <BarChart2 className="w-3.5 h-3.5 text-blue-400" />
          <span>Europe Revenue</span>
        </button>
        <button
          onClick={() => handleSend("Show revenue by region.")}
          className="text-xs bg-gray-900 hover:bg-gray-800 text-gray-300 border border-gray-800 px-3 py-1.5 rounded-full transition-colors flex items-center space-x-1.5"
        >
          <BarChart2 className="w-3.5 h-3.5 text-emerald-400" />
          <span>Revenue by Region</span>
        </button>
        <button
          onClick={() => handleSend("Which product generated the highest revenue?")}
          className="text-xs bg-gray-900 hover:bg-gray-800 text-gray-300 border border-gray-800 px-3 py-1.5 rounded-full transition-colors flex items-center space-x-1.5"
        >
          <BarChart2 className="w-3.5 h-3.5 text-amber-400" />
          <span>Top Product Revenue</span>
        </button>
        <button
          onClick={() => handleSend("What is our profit and margin?")}
          className="text-xs bg-gray-900 hover:bg-gray-800 text-gray-300 border border-gray-800 px-3 py-1.5 rounded-full transition-colors flex items-center space-x-1.5"
        >
          <BarChart2 className="w-3.5 h-3.5 text-purple-400" />
          <span>Profit & Margin</span>
        </button>
        <button
          onClick={() => handleSend("Why did our European margins drop last quarter?")}
          className="text-xs bg-blue-900/30 hover:bg-blue-800/40 text-blue-300 border border-blue-500/30 px-3 py-1.5 rounded-full transition-colors flex items-center space-x-1.5"
        >
          <Sparkles className="w-3.5 h-3.5 text-blue-400" />
          <span>Multi-Step Root Cause Analysis</span>
        </button>
      </div>

      {/* Input Prompt Bar */}
      <div className="p-4 border-t border-gray-800 bg-gray-900/80">
        <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex space-x-3">
          <input
            type="text"
            value={inputPrompt}
            onChange={(e) => setInputPrompt(e.target.value)}
            placeholder="Ask any natural language business question (e.g. 'How much revenue did we make in Europe?')..."
            className="flex-1 bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
          />
          <button
            type="submit"
            disabled={loading || !inputPrompt.trim()}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white px-5 py-3 rounded-xl font-medium text-sm flex items-center space-x-2 transition-colors shadow-lg"
          >
            <span>Ask MetricMind</span>
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
