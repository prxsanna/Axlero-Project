/**
 * MetricMind API Client for FastAPI backend.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface ChatResponse {
  query: string;
  status: string;
  answer?: string;
  metric?: string;
  explanation: string;
  chart_config?: any;
  reasoning_steps: Array<{
    step: number;
    action: string;
    thought?: string;
    query_measures?: string[];
    query_dimensions?: string[];
    generated_sql?: string;
    row_count?: number;
    observation?: string;
  }>;
  transparency: {
    api_calls: Array<{
      step: number;
      request: any;
      sql: string;
    }>;
    governed_metrics_used: string[];
    data_source: string;
    total_rows_scanned: number;
    execution_time_ms: number;
  };
}

export interface MetricDefinition {
  name: string;
  label: string;
  description: string;
  sql_formula: string;
  unit: string;
  format: string;
}

export interface DimensionDefinition {
  name: string;
  label: string;
  sql_column: string;
  type: string;
}

export interface MetricsCatalogResponse {
  measures: Record<string, MetricDefinition>;
  dimensions: Record<string, DimensionDefinition>;
}

export async function sendChatMessage(prompt: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to process query with agent.');
  }

  return response.json();
}

export async function fetchMetricsCatalog(): Promise<MetricsCatalogResponse> {
  const response = await fetch(`${API_BASE_URL}/semantic/metrics`);
  if (!response.ok) {
    throw new Error('Failed to fetch metrics catalog.');
  }
  return response.json();
}
