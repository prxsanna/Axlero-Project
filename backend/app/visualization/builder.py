"""
Apache ECharts Visualization Specification Generator for MetricMind.

Generates structured JSON chart configs rendered dynamically by the frontend.
"""

from typing import List, Dict, Any, Optional

class EChartsBuilder:

    DARK_THEME_COLORS = [
        "#10B981", # Emerald
        "#3B82F6", # Blue
        "#F59E0B", # Amber
        "#8B5CF6", # Purple
        "#EC4899", # Pink
        "#06B6D4", # Cyan
        "#EF4444"  # Red
    ]

    @classmethod
    def build_bar_chart(
        cls,
        title: str,
        data: List[Dict[str, Any]],
        category_dim: str,
        value_cols: List[str]
    ) -> Dict[str, Any]:
        """
        Builds a multi-series or single-series bar chart configuration.
        """
        categories = [str(item.get(category_dim, "")) for item in data]
        series = []

        for idx, col in enumerate(value_cols):
            values = [item.get(col, 0) for item in data]
            series.append({
                "name": col.replace("_", " ").title(),
                "type": "bar",
                "data": values,
                "itemStyle": {
                    "color": cls.DARK_THEME_COLORS[idx % len(cls.DARK_THEME_COLORS)],
                    "borderRadius": [4, 4, 0, 0]
                }
            })

        return {
            "title": {
                "text": title,
                "textStyle": {"color": "#F3F4F6", "fontSize": 15, "fontWeight": 600}
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "backgroundColor": "#1F2937",
                "borderColor": "#374151",
                "textStyle": {"color": "#F3F4F6"}
            },
            "legend": {
                "data": [s["name"] for s in series],
                "textStyle": {"color": "#9CA3AF"},
                "bottom": 0
            },
            "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
            "xAxis": {
                "type": "category",
                "data": categories,
                "axisLabel": {"color": "#9CA3AF", "rotate": 25 if len(categories) > 5 else 0},
                "axisLine": {"lineStyle": {"color": "#4B5563"}}
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {"color": "#9CA3AF"},
                "splitLine": {"lineStyle": {"color": "#374151", "type": "dashed"}}
            },
            "series": series
        }

    @classmethod
    def build_line_chart(
        cls,
        title: str,
        data: List[Dict[str, Any]],
        category_dim: str,
        value_cols: List[str]
    ) -> Dict[str, Any]:
        """
        Builds a trend line chart configuration.
        """
        categories = [str(item.get(category_dim, "")) for item in data]
        series = []

        for idx, col in enumerate(value_cols):
            values = [item.get(col, 0) for item in data]
            series.append({
                "name": col.replace("_", " ").title(),
                "type": "line",
                "smooth": True,
                "data": values,
                "lineStyle": {"width": 3},
                "itemStyle": {"color": cls.DARK_THEME_COLORS[idx % len(cls.DARK_THEME_COLORS)]},
                "areaStyle": {
                    "opacity": 0.15,
                    "color": cls.DARK_THEME_COLORS[idx % len(cls.DARK_THEME_COLORS)]
                }
            })

        return {
            "title": {
                "text": title,
                "textStyle": {"color": "#F3F4F6", "fontSize": 15, "fontWeight": 600}
            },
            "tooltip": {
                "trigger": "axis",
                "backgroundColor": "#1F2937",
                "borderColor": "#374151",
                "textStyle": {"color": "#F3F4F6"}
            },
            "legend": {
                "data": [s["name"] for s in series],
                "textStyle": {"color": "#9CA3AF"},
                "bottom": 0
            },
            "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
            "xAxis": {
                "type": "category",
                "data": categories,
                "axisLabel": {"color": "#9CA3AF"},
                "axisLine": {"lineStyle": {"color": "#4B5563"}}
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {"color": "#9CA3AF"},
                "splitLine": {"lineStyle": {"color": "#374151", "type": "dashed"}}
            },
            "series": series
        }

    @classmethod
    def build_pie_chart(
        cls,
        title: str,
        data: List[Dict[str, Any]],
        category_dim: str,
        value_col: str
    ) -> Dict[str, Any]:
        """
        Builds a donut / pie chart configuration.
        """
        pie_data = [
            {"name": str(item.get(category_dim, "")), "value": item.get(value_col, 0)}
            for item in data
        ]

        return {
            "title": {
                "text": title,
                "textStyle": {"color": "#F3F4F6", "fontSize": 15, "fontWeight": 600}
            },
            "tooltip": {
                "trigger": "item",
                "formatter": "{b}: {c} ({d}%)",
                "backgroundColor": "#1F2937",
                "borderColor": "#374151",
                "textStyle": {"color": "#F3F4F6"}
            },
            "legend": {
                "orient": "horizontal",
                "bottom": 0,
                "textStyle": {"color": "#9CA3AF"}
            },
            "series": [
                {
                    "name": value_col.replace("_", " ").title(),
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "avoidLabelOverlap": False,
                    "itemStyle": {
                        "borderRadius": 6,
                        "borderColor": "#111827",
                        "borderWidth": 2
                    },
                    "label": {"show": False},
                    "emphasis": {
                        "label": {"show": True, "fontSize": 14, "fontWeight": "bold", "color": "#F3F4F6"}
                    },
                    "data": pie_data
                }
            ]
        }
