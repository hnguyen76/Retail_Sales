const data = window.RETAIL_SALES_DATA;

const colors = {
  blue: "#2563eb",
  teal: "#0f766e",
  coral: "#e45745",
  gold: "#c58b12",
  green: "#23845f",
  ink: "#172026",
  muted: "#65707a",
  line: "#dfd8ce",
};

const palette = [
  colors.blue,
  colors.teal,
  colors.coral,
  colors.gold,
  colors.green,
  "#7c3aed",
  "#db2777",
  "#475569",
];

const state = {
  view: "All",
  metric: "revenue",
};

const els = {
  year: document.querySelector("#yearFilter"),
  metric: document.querySelector("#metricFilter"),
  period: document.querySelector("#period"),
  kpis: document.querySelector("#kpis"),
  insights: document.querySelector("#insights"),
  productList: document.querySelector("#productList"),
  discountBody: document.querySelector("#discountBody"),
  trend: document.querySelector("#trendChart"),
  category: document.querySelector("#categoryChart"),
  channel: document.querySelector("#channelChart"),
  region: document.querySelector("#regionChart"),
};

const money = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

const compactMoney = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  notation: "compact",
  maximumFractionDigits: 2,
});

const compact = new Intl.NumberFormat("en-US", {
  notation: "compact",
  maximumFractionDigits: 1,
});

const number = new Intl.NumberFormat("en-US");

function viewData() {
  return data.views[state.view];
}

function resizeCanvas(canvas) {
  const ratio = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = Math.round(rect.width * ratio);
  canvas.height = Math.round(rect.height * ratio);
  const ctx = canvas.getContext("2d");
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  return { ctx, width: rect.width, height: rect.height };
}

function clear(ctx, width, height) {
  ctx.clearRect(0, 0, width, height);
}

function drawText(ctx, text, x, y, options = {}) {
  ctx.save();
  ctx.fillStyle = options.color || colors.ink;
  ctx.font = `${options.weight || 600} ${options.size || 12}px Inter, Segoe UI, sans-serif`;
  ctx.textAlign = options.align || "left";
  ctx.textBaseline = options.baseline || "middle";
  ctx.fillText(text, x, y);
  ctx.restore();
}

function drawTrend(canvas, rows) {
  const { ctx, width, height } = resizeCanvas(canvas);
  clear(ctx, width, height);
  const pad = { top: 18, right: 20, bottom: 42, left: 64 };
  const plotW = width - pad.left - pad.right;
  const plotH = height - pad.top - pad.bottom;
  const values = rows.map((row) => row[state.metric]);
  const max = Math.max(...values) * 1.08;
  const min = 0;

  ctx.strokeStyle = "rgba(101, 112, 122, 0.22)";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i += 1) {
    const y = pad.top + (plotH / 4) * i;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(width - pad.right, y);
    ctx.stroke();
    const labelValue = max - ((max - min) / 4) * i;
    drawText(
      ctx,
      state.metric === "revenue" ? compactMoney.format(labelValue) : compact.format(labelValue),
      pad.left - 10,
      y,
      { align: "right", color: colors.muted, size: 11, weight: 600 },
    );
  }

  const points = rows.map((row, index) => {
    const x = pad.left + (plotW / Math.max(rows.length - 1, 1)) * index;
    const y = pad.top + plotH - ((row[state.metric] - min) / (max - min || 1)) * plotH;
    return { x, y, row };
  });

  const gradient = ctx.createLinearGradient(0, pad.top, 0, pad.top + plotH);
  gradient.addColorStop(0, "rgba(37, 99, 235, 0.22)");
  gradient.addColorStop(1, "rgba(37, 99, 235, 0)");

  ctx.beginPath();
  points.forEach((point, index) => {
    if (index === 0) ctx.moveTo(point.x, point.y);
    else ctx.lineTo(point.x, point.y);
  });
  ctx.lineTo(points[points.length - 1].x, pad.top + plotH);
  ctx.lineTo(points[0].x, pad.top + plotH);
  ctx.closePath();
  ctx.fillStyle = gradient;
  ctx.fill();

  ctx.beginPath();
  points.forEach((point, index) => {
    if (index === 0) ctx.moveTo(point.x, point.y);
    else ctx.lineTo(point.x, point.y);
  });
  ctx.strokeStyle = colors.blue;
  ctx.lineWidth = 3;
  ctx.stroke();

  points.forEach((point, index) => {
    if (index % Math.ceil(points.length / 8) === 0 || index === points.length - 1) {
      drawText(ctx, point.row.month.slice(2), point.x, height - 20, {
        align: "center",
        color: colors.muted,
        size: 11,
      });
    }
    ctx.beginPath();
    ctx.arc(point.x, point.y, 3.5, 0, Math.PI * 2);
    ctx.fillStyle = colors.blue;
    ctx.fill();
  });
}

function drawHorizontalBars(canvas, rows, key = "revenue") {
  const { ctx, width, height } = resizeCanvas(canvas);
  clear(ctx, width, height);
  const pad = { top: 12, right: 24, bottom: 20, left: 112 };
  const max = Math.max(...rows.map((row) => row[key]));
  const rowH = (height - pad.top - pad.bottom) / rows.length;

  rows.forEach((row, index) => {
    const y = pad.top + index * rowH + rowH / 2;
    const barW = ((width - pad.left - pad.right) * row[key]) / max;
    drawText(ctx, row.name, pad.left - 10, y, {
      align: "right",
      color: colors.ink,
      size: 12,
      weight: 700,
    });
    ctx.fillStyle = "rgba(223, 216, 206, 0.75)";
    ctx.fillRect(pad.left, y - 9, width - pad.left - pad.right, 18);
    ctx.fillStyle = palette[index % palette.length];
    ctx.fillRect(pad.left, y - 9, barW, 18);
    drawText(ctx, compactMoney.format(row[key]), pad.left + barW + 8, y, {
      color: colors.muted,
      size: 11,
      weight: 700,
    });
  });
}

function drawDonut(canvas, rows) {
  const { ctx, width, height } = resizeCanvas(canvas);
  clear(ctx, width, height);
  const total = rows.reduce((sum, row) => sum + row.revenue, 0);
  const cx = Math.min(width * 0.34, 132);
  const cy = height / 2;
  const radius = Math.min(height * 0.32, width * 0.24);
  const inner = radius * 0.58;
  let start = -Math.PI / 2;

  rows.forEach((row, index) => {
    const angle = (row.revenue / total) * Math.PI * 2;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, start, start + angle);
    ctx.arc(cx, cy, inner, start + angle, start, true);
    ctx.closePath();
    ctx.fillStyle = palette[index % palette.length];
    ctx.fill();
    start += angle;
  });

  drawText(ctx, compactMoney.format(total), cx, cy - 6, { align: "center", size: 20, weight: 800 });
  drawText(ctx, "sales", cx, cy + 18, { align: "center", color: colors.muted, size: 12 });

  const legendX = Math.min(width * 0.62, width - 170);
  rows.forEach((row, index) => {
    const y = cy - rows.length * 18 + index * 36 + 10;
    ctx.fillStyle = palette[index % palette.length];
    ctx.fillRect(legendX, y - 7, 14, 14);
    drawText(ctx, row.name, legendX + 24, y - 2, { size: 13, weight: 800 });
    drawText(ctx, `${row.share.toFixed(1)}%`, legendX + 24, y + 15, {
      size: 11,
      color: colors.muted,
      weight: 700,
    });
  });
}

function renderKpis(d) {
  const k = d.kpis;
  const cards = [
    ["Net Sales", compactMoney.format(k.revenue), `${state.view} performance`],
    ["Transactions", compact.format(k.transactions), `${number.format(k.units)} units sold`],
    ["Average Order", money.format(k.averageOrderValue), `${money.format(k.averageSellingPrice)} per unit`],
    ["Customers", compact.format(k.customers), `${number.format(k.products)} products tracked`],
    ["Discount Rate", `${k.effectiveDiscountRate.toFixed(2)}%`, `${money.format(k.discountValue)} discount value`],
    ["YoY Growth", `${(data.views.All.kpis.yoyRevenueGrowth || 0).toFixed(2)}%`, "2025 revenue vs 2024"],
  ];
  els.kpis.innerHTML = cards
    .map(
      ([label, value, note]) => `
        <article class="kpi">
          <span>${label}</span>
          <strong>${value}</strong>
          <em>${note}</em>
        </article>
      `,
    )
    .join("");
}

function renderProducts(rows) {
  const max = Math.max(...rows.map((row) => row.revenue));
  els.productList.innerHTML = rows
    .slice(0, 8)
    .map(
      (row, index) => `
      <div class="rank-row">
        <span class="rank">${index + 1}</span>
        <strong>${row.name}</strong>
        <span>${compactMoney.format(row.revenue)}</span>
        <span class="bar-track"><i style="width:${(row.revenue / max) * 100}%"></i></span>
      </div>
    `,
    )
    .join("");
}

function renderDiscount(rows) {
  els.discountBody.innerHTML = rows
    .map(
      (row) => `
      <tr>
        <td>${row.discountPct}%</td>
        <td>${money.format(row.revenue)}</td>
        <td>${number.format(row.transactions)}</td>
        <td>${row.share.toFixed(2)}%</td>
      </tr>
    `,
    )
    .join("");
}

function renderInsights(d) {
  const category = d.category[0];
  const channel = d.channel[0];
  const region = d.region[0];
  els.insights.innerHTML = `
    <div class="insight">
      <div><strong>${category.name} leads the portfolio</strong><span>${category.name} produces ${compactMoney.format(category.revenue)} in revenue, equal to ${category.share.toFixed(1)}% of total sales.</span></div>
    </div>
    <div class="insight">
      <div><strong>${channel.name} is the top channel</strong><span>The three channels are tightly balanced, so merchandising and conversion improvements can shift share quickly.</span></div>
    </div>
    <div class="insight">
      <div><strong>${region.name} is the strongest region</strong><span>${region.name} contributes ${compactMoney.format(region.revenue)}, while the remaining regions stay close enough for repeatable playbooks.</span></div>
    </div>
  `;
}

function render() {
  const d = viewData();
  els.period.textContent = `${data.metadata.dateRange.start} to ${data.metadata.dateRange.end}`;
  renderKpis(d);
  renderProducts(d.topProducts);
  renderDiscount(d.discount);
  renderInsights(d);
  drawTrend(els.trend, d.monthly);
  drawHorizontalBars(els.category, d.category);
  drawDonut(els.channel, d.channel);
  drawHorizontalBars(els.region, d.region);
}

function init() {
  Object.keys(data.views).forEach((view) => {
    const option = document.createElement("option");
    option.value = view;
    option.textContent = view === "All" ? "All Years" : view;
    els.year.appendChild(option);
  });

  els.year.addEventListener("change", (event) => {
    state.view = event.target.value;
    render();
  });

  els.metric.addEventListener("change", (event) => {
    state.metric = event.target.value;
    render();
  });

  window.addEventListener("resize", render);
  render();
}

init();
