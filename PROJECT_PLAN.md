# Retail Sales Dashboard Project Plan

Muc tieu cua GitHub Project nay la quan ly nhung viec tiep theo de bien repo
`Retail_Sales` thanh mot portfolio project chuyen nghiep: co dashboard, bao cao,
du lieu tom tat, tai lieu ro rang, va quy trinh phat trien de nguoi xem GitHub
thay duoc cach ban lam viec.

## Project Setup Tren GitHub

Tao Project trong tab **Projects** voi cac cot:

| Column | Dung de lam gi |
| --- | --- |
| Todo | Viec da len y tuong nhung chua lam |
| In Progress | Viec dang lam |
| Review | Viec da xong can kiem tra lai |
| Done | Viec da hoan thanh |

Nen them cac field:

| Field | Gia tri goi y |
| --- | --- |
| Priority | High, Medium, Low |
| Area | Dashboard, Data, Documentation, Deployment |
| Status | Todo, In Progress, Review, Done |
| Due Date | Ngay du kien hoan thanh |

## Roadmap

| Phase | Goal | Outcome |
| --- | --- | --- |
| Phase 1 | Hoan thien dashboard hien tai | Dashboard ro rang, responsive, co credit |
| Phase 2 | Cai thien tai lieu | README co screenshot, huong dan mo dashboard, insight mau |
| Phase 3 | Deployment | Bat GitHub Pages de xem dashboard bang link public |
| Phase 4 | Analytics polish | Them forecast, so sanh theo segment, insight nang cao |
| Phase 5 | Portfolio packaging | Them case study, anh demo, va mo ta business impact |

## Suggested Issues

### 1. Enable GitHub Pages Deployment

**Priority:** High  
**Area:** Deployment  
**Status:** Todo

Acceptance criteria:

- GitHub Pages is enabled from the `main` branch.
- `index.html` opens correctly from the public GitHub Pages URL.
- README includes the live dashboard link.

### 2. Add Dashboard Screenshot To README

**Priority:** High  
**Area:** Documentation  
**Status:** Todo

Acceptance criteria:

- A screenshot is saved under `assets/`.
- README shows the screenshot near the top.
- README explains what the dashboard measures.

### 3. Add Vietnamese Executive Summary

**Priority:** Medium  
**Area:** Documentation  
**Status:** Todo

Acceptance criteria:

- Add `reports/retail_sales_executive_report_vi.md`.
- Translate the executive summary and recommendations.
- Keep business terms clear and professional.

### 4. Add Forecast Section

**Priority:** Medium  
**Area:** Dashboard  
**Status:** Todo

Acceptance criteria:

- Add a simple three-month revenue forecast.
- Explain the method in the report.
- Show forecast values in the dashboard without cluttering the layout.

### 5. Add Customer Segment Deep Dive

**Priority:** Medium  
**Area:** Analytics  
**Status:** Todo

Acceptance criteria:

- Add segment-level revenue, AOV, transaction count, and customer count.
- Add a chart or table to the dashboard.
- Include one recommendation based on customer segment behavior.

### 6. Add Data Quality Checks

**Priority:** Low  
**Area:** Data  
**Status:** Todo

Acceptance criteria:

- Script checks missing values, negative sales, invalid discount rates, and date range.
- Results are written to a summary section in the report.
- README explains how to rerun the checks.

## Cach Dung De Hoc Theo

1. Tao GitHub Project moi trong tab **Projects**.
2. Them cac issue trong phan **Suggested Issues** vao project.
3. Dat cot ban dau la `Todo`.
4. Khi lam mot task, keo sang `In Progress`.
5. Khi code xong, keo sang `Review`.
6. Khi da commit/push va kiem tra, keo sang `Done`.

Day la cach lam giong workflow thuc te: y tuong duoc ghi thanh issue, issue duoc
dua vao project board, code duoc commit vao repo, va ket qua duoc cap nhat lai
trong README/report.
