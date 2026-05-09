# Retail Sales Intelligence Dashboard
https://hnguyen76.github.io/Retail_Sales/

Professional retail sales analysis package built from `retail_sales_dataset.csv`.

## What Is Included

- `index.html` - interactive browser dashboard with KPI cards, trend analysis, category/channel/region views, top products, discount analysis, and footer credit.
- `reports/retail_sales_executive_report.md` - executive report with findings and recommendations.
- `reports/*.csv` - clean summary exports for monthly sales, category performance, top products, and discount tiers.
- `data/retail_sales_summary.json` - machine-readable summary data.
- `data/retail_sales_summary.js` - browser-ready data used by the dashboard.
- `scripts/build_retail_report.py` - reproducible analysis script using only the Python standard library.
- `PROJECT_PLAN.md` - sample GitHub Project roadmap and issue plan.
- `.github/ISSUE_TEMPLATE/project_task.md` - reusable issue template for Project tasks.
- `docs/github-project-guide.md` - step-by-step guide for creating the GitHub Project board.

## Open The Dashboard

Open `index.html` in a browser. The dashboard is static and does not require a server or package installation.

## Rebuild The Report

```bash
python scripts/build_retail_report.py
```

The script reads `retail_sales_dataset.csv` and regenerates the files in `data/` and `reports/`.

## Dashboard Credit

Created by Hieu Nguyen
