from pydantic import BaseModel
from typing import List, Literal
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -----------------------------
# Pydantic Models
# -----------------------------

class TimeSeriesPoint(BaseModel):
    timestamp: date
    value: float

class MetricSeries(BaseModel):
    label: str
    data: List[TimeSeriesPoint]
    is_forecast: bool = False

class ChartData(BaseModel):
    title: str
    x_axis_label: str
    y_axis_label: str
    series: List[MetricSeries]

class CompetitorAnalysisInput(BaseModel):
    company_name: str
    competitor_names: List[str]
    region: str
    date_range_start: date
    date_range_end: date
    forecast_periods: int = 3
    frequency: Literal['monthly', 'quarterly'] = 'monthly'
    
    clickstream_chart: ChartData
    revenue_chart: ChartData
    traffic_chart: ChartData


# -----------------------------
# Plotting Function
# -----------------------------

def plot_chart(chart: ChartData):
    plt.figure(figsize=(10, 6))
    for series in chart.series:
        x = [point.timestamp for point in series.data]
        y = [point.value for point in series.data]
        linestyle = '--' if series.is_forecast else '-'
        plt.plot(x, y, label=series.label, linestyle=linestyle)
    
    plt.title(chart.title)
    plt.xlabel(chart.x_axis_label)
    plt.ylabel(chart.y_axis_label)
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()


def plot_all_charts(data: CompetitorAnalysisInput):
    plot_chart(data.clickstream_chart)
    plot_chart(data.revenue_chart)
    plot_chart(data.traffic_chart)


# -----------------------------
# Sample Input Data
# -----------------------------

def generate_time_series(start: date, periods: int, freq: str, base_value: float, delta: float, forecast=False) -> List[TimeSeriesPoint]:
    results = []
    current = start
    for i in range(periods):
        value = base_value + (i * delta)
        results.append(TimeSeriesPoint(timestamp=current, value=value))
        if freq == 'monthly':
            current = current.replace(month=current.month % 12 + 1, year=current.year + (current.month // 12))
        elif freq == 'quarterly':
            current = current.replace(month=current.month + 3 if current.month <= 9 else 1, year=current.year + (1 if current.month > 9 else 0))
    return results


def build_sample_input() -> CompetitorAnalysisInput:
    start_date = date(2024, 1, 1)
    historical_periods = 6
    forecast_periods = 3
    freq = 'monthly'

    def make_series(metric_name, base, delta, forecast_delta=0.5):
        return [
            MetricSeries(
                label=f"{metric_name} - {company}",
                data=generate_time_series(start_date, historical_periods, freq, base + i*10, delta),
                is_forecast=False
            )
            for i, company in enumerate(["YourBrand", "CompA", "CompB"])
        ] + [
            MetricSeries(
                label=f"{metric_name} - {company} (Forecast)",
                data=generate_time_series(
                    start_date.replace(month=start_date.month + historical_periods),
                    forecast_periods, freq, base + i*10 + historical_periods * delta, forecast_delta
                ),
                is_forecast=True
            )
            for i, company in enumerate(["YourBrand", "CompA", "CompB"])
        ]

    return CompetitorAnalysisInput(
        company_name="YourBrand",
        competitor_names=["CompA", "CompB"],
        region="Southeast Asia",
        date_range_start=start_date,
        date_range_end=start_date.replace(month=start_date.month + historical_periods - 1),
        forecast_periods=forecast_periods,
        frequency=freq,
        
        clickstream_chart=ChartData(
            title="Clickstream Metrics Over Time",
            x_axis_label="Time",
            y_axis_label="Value",
            series=make_series("Total Visits", 1000, 100)
        ),
        
        revenue_chart=ChartData(
            title="Monthly Revenue Trends",
            x_axis_label="Time",
            y_axis_label="Revenue ($)",
            series=make_series("Revenue", 50000, 3000)
        ),
        
        traffic_chart=ChartData(
            title="Traffic Sources Over Time",
            x_axis_label="Time",
            y_axis_label="Traffic Volume",
            series=make_series("Direct Traffic", 2000, 150)
        )
    )


# -----------------------------
# Run the Script
# -----------------------------

if __name__ == "__main__":
    input_data = build_sample_input()
    plot_all_charts(input_data)
