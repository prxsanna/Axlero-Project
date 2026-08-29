"""
Pydantic Schemas for MetricMind Semantic Layer.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class FilterCondition(BaseModel):
    dimension: str = Field(..., description="Target dimension name e.g. 'region', 'product'")
    operator: str = Field("=", description="Filter operator e.g. '=', '!=', 'IN', 'LIKE', '>=', '<='")
    value: Any = Field(..., description="Filter value or list of values e.g. 'Europe', ['Asia', 'Europe']")

class SemanticQueryRequest(BaseModel):
    measures: List[str] = Field(..., description="List of governed metrics e.g. ['revenue', 'margin_pct']")
    dimensions: Optional[List[str]] = Field(default=[], description="List of dimensions to group by e.g. ['region', 'quarter']")
    filters: Optional[List[FilterCondition]] = Field(default=[], description="List of filter conditions")
    limit: Optional[int] = Field(default=100, description="Max rows to return (capped at 1000)")
    order_by: Optional[str] = Field(default=None, description="Optional column to order by")
    order_desc: Optional[bool] = Field(default=True, description="Order descending if True")

class SemanticQueryResponse(BaseModel):
    status: str = Field("success", description="Status of query execution: 'success' or 'error'")
    measures: List[str]
    dimensions: List[str]
    generated_sql: str = Field(..., description="Governed SQL compiled and executed against PostgreSQL")
    data: List[Dict[str, Any]] = Field(..., description="Structured JSON query results")
    row_count: int
    execution_time_ms: float
    governance_passed: bool
    data_source: str = Field("PostgreSQL (metricmind)", description="Database engine source")
    error_message: Optional[str] = None
