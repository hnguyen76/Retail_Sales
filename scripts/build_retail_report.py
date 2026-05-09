from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "retail_sales_dataset.csv"
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"


MONEY = Decimal("0.01")


def money(value: Decimal) -> float:
    return float(value.quantize(MONEY, rounding=ROUND_HALF_UP))


def pct(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def top_items(mapping: dict[str, Decimal], limit: int | None = None) -> list[dict[str, object]]:
    ranked = sorted(mapping.items(), key=lambda item: item[1], reverse=True)
    if limit is not None:
        ranked = ranked[:limit]
    total = sum(mapping.values(), Decimal("0"))
    return [
        {
            "name": name,
            "revenue": money(value),
            "share": pct((value / total * 100) if total else Decimal("0")),
        }
        for name, value in ranked
    ]


@dataclass
class Summary:
    revenue: Decimal = Decimal("0")
    transactions: int = 0
    units: int = 0
    gross_sales: Decimal = Decimal("0")
    discount_value: Decimal = Decimal("0")
    customers: set[str] = field(default_factory=set)
    products: set[str] = field(default_factory=set)
    monthly_revenue: dict[str, Decimal] = field(default_factory=lambda: defaultdict(Decimal))
    monthly_transactions: Counter[str] = field(default_factory=Counter)
    category_revenue: dict[str, Decimal] = field(default_factory=lambda: defaultdict(Decimal))
    channel_revenue: dict[str, Decimal] = field(default_factory=lambda: defaultdict(Decimal))
    region_revenue: dict[str, Decimal] = field(default_factory=lambda: defaultdict(Decimal))
    segment_revenue: dict[str, Decimal] = field(default_factory=lambda: defaultdict(Decimal))
    payment_revenue: dict[str, Decimal] = field(default_factory=lambda: defaultdict(Decimal))
    age_revenue: dict[str, Decimal] = field(default_factory=lambda: defaultdict(Decimal))
    gender_revenue: dict[str, Decimal] = field(default_factory=lambda: defaultdict(Decimal))
    product_revenue: dict[str, Decimal] = field(default_factory=lambda: defaultdict(Decimal))
    product_units: Counter[str] = field(default_factory=Counter)
    discount_revenue: dict[str, Decimal] = field(default_factory=lambda: defaultdict(Decimal))
    discount_transactions: Counter[str] = field(default_factory=Counter)

    def add(self, row: dict[str, str]) -> None:
        sale = Decimal(row["sales_amount"])
        quantity = int(row["quantity"])
        unit_price = Decimal(row["unit_price"])
        gross = unit_price * quantity
        month = row["transaction_date"][:7]

        self.revenue += sale
        self.transactions += 1
        self.units += quantity
        self.gross_sales += gross
        self.discount_value += gross - sale
        self.customers.add(row["customer_id"])
        self.products.add(row["product_id"])
        self.monthly_revenue[month] += sale
        self.monthly_transactions[month] += 1
        self.category_revenue[row["category"]] += sale
        self.channel_revenue[row["sales_channel"]] += sale
        self.region_revenue[row["region"]] += sale
        self.segment_revenue[row["customer_segment"]] += sale
        self.payment_revenue[row["payment_method"]] += sale
        self.age_revenue[row["customer_age_group"]] += sale
        self.gender_revenue[row["customer_gender"]] += sale
        self.product_revenue[row["product_name"]] += sale
        self.product_units[row["product_name"]] += quantity
        self.discount_revenue[row["discount_pct"]] += sale
        self.discount_transactions[row["discount_pct"]] += 1

    def as_dict(self, label: str) -> dict[str, object]:
        avg_order = self.revenue / self.transactions if self.transactions else Decimal("0")
        avg_unit_price = self.revenue / self.units if self.units else Decimal("0")
        discount_rate = self.discount_value / self.gross_sales * 100 if self.gross_sales else Decimal("0")
        return {
            "label": label,
            "kpis": {
                "revenue": money(self.revenue),
                "transactions": self.transactions,
                "units": self.units,
                "customers": len(self.customers),
                "products": len(self.products),
                "averageOrderValue": money(avg_order),
                "averageSellingPrice": money(avg_unit_price),
                "grossSales": money(self.gross_sales),
                "discountValue": money(self.discount_value),
                "effectiveDiscountRate": pct(discount_rate),
            },
            "monthly": [
                {
                    "month": month,
                    "revenue": money(self.monthly_revenue[month]),
                    "transactions": self.monthly_transactions[month],
                }
                for month in sorted(self.monthly_revenue)
            ],
            "category": top_items(self.category_revenue),
            "channel": top_items(self.channel_revenue),
            "region": top_items(self.region_revenue),
            "segment": top_items(self.segment_revenue),
            "payment": top_items(self.payment_revenue),
            "age": top_items(self.age_revenue),
            "gender": top_items(self.gender_revenue),
            "topProducts": [
                {
                    "name": name,
                    "revenue": money(value),
                    "units": self.product_units[name],
                    "share": pct((value / self.revenue * 100) if self.revenue else Decimal("0")),
                }
                for name, value in sorted(
                    self.product_revenue.items(), key=lambda item: item[1], reverse=True
                )[:12]
            ],
            "discount": [
                {
                    "discountPct": int(discount),
                    "revenue": money(value),
                    "transactions": self.discount_transactions[discount],
                    "share": pct((value / self.revenue * 100) if self.revenue else Decimal("0")),
                }
                for discount, value in sorted(
                    self.discount_revenue.items(), key=lambda item: int(item[0])
                )
            ],
        }


def format_currency(value: float | Decimal) -> str:
    amount = Decimal(str(value))
    if amount >= Decimal("1000000"):
        return f"${amount / Decimal('1000000'):.2f}M"
    if amount >= Decimal("1000"):
        return f"${amount / Decimal('1000'):.1f}K"
    return f"${amount:.2f}"


def format_int(value: int) -> str:
    return f"{value:,}"


def write_json(summary: dict[str, object]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    json_path = DATA_DIR / "retail_sales_summary.json"
    js_path = DATA_DIR / "retail_sales_summary.js"
    payload = json.dumps(summary, indent=2)
    json_path.write_text(payload + "\n", encoding="utf-8")
    js_path.write_text(f"window.RETAIL_SALES_DATA = {payload};\n", encoding="utf-8")


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary_tables(summary: dict[str, object]) -> None:
    all_data = summary["views"]["All"]
    write_csv(
        REPORTS_DIR / "monthly_sales.csv",
        all_data["monthly"],
        ["month", "revenue", "transactions"],
    )
    write_csv(
        REPORTS_DIR / "category_performance.csv",
        all_data["category"],
        ["name", "revenue", "share"],
    )
    write_csv(
        REPORTS_DIR / "top_products.csv",
        all_data["topProducts"],
        ["name", "revenue", "units", "share"],
    )
    write_csv(
        REPORTS_DIR / "discount_performance.csv",
        all_data["discount"],
        ["discountPct", "revenue", "transactions", "share"],
    )


def calc_yoy(current: Decimal, prior: Decimal) -> Decimal:
    if not prior:
        return Decimal("0")
    return (current - prior) / prior * 100


def write_markdown_report(summary: dict[str, object]) -> None:
    all_data = summary["views"]["All"]
    y2024 = summary["views"]["2024"]["kpis"]
    y2025 = summary["views"]["2025"]["kpis"]
    yoy = calc_yoy(Decimal(str(y2025["revenue"])), Decimal(str(y2024["revenue"])))
    top_category = all_data["category"][0]
    top_product = all_data["topProducts"][0]
    top_channel = all_data["channel"][0]
    top_region = all_data["region"][0]
    kpis = all_data["kpis"]

    markdown = f"""# Retail Sales Executive Report

## Executive Summary

This report analyzes **{format_int(kpis["transactions"])} retail transactions** from **{summary["metadata"]["dateRange"]["start"]} to {summary["metadata"]["dateRange"]["end"]}**. Total net sales reached **{format_currency(kpis["revenue"])}** across **{format_int(kpis["units"])} units**, with an average order value of **{format_currency(kpis["averageOrderValue"])}**.

Revenue is balanced across stores, channels, and customer segments, which indicates a resilient sales base rather than dependence on one narrow source. The highest-grossing category is **{top_category["name"]}** at **{format_currency(top_category["revenue"])}**, while the top product is **{top_product["name"]}** at **{format_currency(top_product["revenue"])}**.

## Key Performance Indicators

| Metric | Result |
| --- | ---: |
| Net sales | {format_currency(kpis["revenue"])} |
| Gross sales before discount | {format_currency(kpis["grossSales"])} |
| Discount value | {format_currency(kpis["discountValue"])} |
| Effective discount rate | {kpis["effectiveDiscountRate"]:.2f}% |
| Transactions | {format_int(kpis["transactions"])} |
| Units sold | {format_int(kpis["units"])} |
| Unique customers | {format_int(kpis["customers"])} |
| Average order value | {format_currency(kpis["averageOrderValue"])} |
| 2025 vs 2024 revenue growth | {yoy:.2f}% |

## Performance Highlights

- **Category leader:** {top_category["name"]} contributes {top_category["share"]:.2f}% of sales.
- **Channel leader:** {top_channel["name"]} contributes {top_channel["share"]:.2f}% of sales.
- **Regional leader:** {top_region["name"]} contributes {top_region["share"]:.2f}% of sales.
- **Product leader:** {top_product["name"]} contributes {top_product["share"]:.2f}% of sales and {format_int(top_product["units"])} units.
- **Customer mix:** Loyal, New, VIP, and Returning segments each contribute close to one quarter of sales, suggesting broad customer coverage.

## Recommendations

1. Protect the top categories while testing targeted growth plays in Clothing, which trails the rest of the portfolio.
2. Maintain a balanced channel strategy; In-Store, Mobile App, and Online sales are close enough that execution quality can move share quickly.
3. Review discount tiers above 20%. They represent a smaller share of revenue and should be tied to clear inventory or acquisition goals.
4. Use top-product bundles around Bread, Lipstick, Textbook, Smartphone, and Water Bottle to lift average order value.
5. Track monthly revenue variance and build a forecast layer once more seasonal history is available.

## Included Files

| File | Purpose |
| --- | --- |
| `index.html` | Interactive dashboard |
| `data/retail_sales_summary.json` | Machine-readable dashboard data |
| `data/retail_sales_summary.js` | Browser-ready dashboard data |
| `reports/monthly_sales.csv` | Monthly revenue and transaction summary |
| `reports/category_performance.csv` | Category revenue ranking |
| `reports/top_products.csv` | Product ranking |
| `reports/discount_performance.csv` | Discount tier performance |
| `scripts/build_retail_report.py` | Reproducible analysis script |

Generated by the retail sales reporting workflow.
"""
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / "retail_sales_executive_report.md").write_text(markdown, encoding="utf-8")


def build_summary() -> dict[str, object]:
    summaries = {"All": Summary(), "2024": Summary(), "2025": Summary()}
    start_date = None
    end_date = None

    with SOURCE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = datetime.strptime(row["transaction_date"], "%Y-%m-%d").date()
            start_date = date if start_date is None or date < start_date else start_date
            end_date = date if end_date is None or date > end_date else end_date
            year = str(date.year)
            summaries["All"].add(row)
            if year in summaries:
                summaries[year].add(row)

    views = {label: summary.as_dict(label) for label, summary in summaries.items()}
    revenue_2024 = summaries["2024"].revenue
    revenue_2025 = summaries["2025"].revenue
    views["All"]["kpis"]["yoyRevenueGrowth"] = pct(calc_yoy(revenue_2025, revenue_2024))

    return {
        "metadata": {
            "source": SOURCE.name,
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "dateRange": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None,
            },
        },
        "views": views,
    }


def main() -> None:
    summary = build_summary()
    write_json(summary)
    write_summary_tables(summary)
    write_markdown_report(summary)
    print("Generated retail sales dashboard data and report files.")


if __name__ == "__main__":
    main()
