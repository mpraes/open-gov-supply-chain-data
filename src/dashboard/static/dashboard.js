const body = document.body;
const kpiUrl = body.dataset.kpiUrl;
const emptyState = document.getElementById("empty-state");
const cardsEl = document.getElementById("kpi-cards");
const rankedLeft = document.getElementById("ranked-left");
const rankedRight = document.getElementById("ranked-right");
const boardLeft = document.getElementById("leaderboard-left");
const boardRight = document.getElementById("leaderboard-right");
const timeframeEl = document.getElementById("timeframe");
let chart;

const THEME_HEADINGS = {
  fornecedor: ["UF", "Porte", "Fornecedores", "CNAEs"],
  material: ["Grupos (itens)", "Grupos (spend)", "Itens", "Fornecedores"],
  servico: ["Seções", "Grupos (spend)", "Serviços", "Fornecedores"],
  uasg: ["UF", "SISG", "UASGs", "Órgãos"],
};

function applyThemeHeadings() {
  const titles = THEME_HEADINGS[body.dataset.theme];
  if (!titles) {
    return;
  }
  document.getElementById("ranked-left-title").textContent = titles[0];
  document.getElementById("ranked-right-title").textContent = titles[1];
  document.getElementById("board-left-title").textContent = titles[2];
  document.getElementById("board-right-title").textContent = titles[3];
}

function dashCards() {
  cardsEl.innerHTML = "";
  for (let i = 0; i < 6; i += 1) {
    cardsEl.appendChild(cardNode("—", "—", ""));
  }
}

function cardNode(label, value, hint) {
  const article = document.createElement("article");
  article.className = "card";
  article.innerHTML =
    `<div class="label"></div><div class="value"></div><div class="hint"></div>`;
  article.querySelector(".label").textContent = label;
  article.querySelector(".value").textContent = value;
  article.querySelector(".hint").textContent = hint;
  return article;
}

function renderCards(cards) {
  cardsEl.innerHTML = "";
  cards.forEach((card) => {
    cardsEl.appendChild(cardNode(card.label, card.value, card.hint));
  });
}

function renderRanked(target, rows) {
  target.innerHTML = "";
  rows.forEach((row) => {
    const item = document.createElement("li");
    const fill = document.createElement("span");
    fill.style.width = `${row.pct}%`;
    item.innerHTML = (
      `<div><strong></strong><div class="bar"></div></div>`
      + `<span class="rank-value"></span>`
    );
    item.querySelector("strong").textContent = row.label;
    item.querySelector(".bar").appendChild(fill);
    item.querySelector(".rank-value").textContent = row.value;
    target.appendChild(item);
  });
}

function renderBoard(target, rows) {
  target.innerHTML = "";
  rows.forEach((row) => {
    const item = document.createElement("li");
    item.innerHTML = `<div><strong></strong><div class="hint"></div></div><span></span>`;
    item.querySelector("strong").textContent = row.title;
    item.querySelector(".hint").textContent = row.subtitle;
    item.querySelector("span").textContent = String(row.rank);
    target.appendChild(item);
  });
}

function chartSeries(series, periods) {
  return series.map((s) => {
    const byPeriod = Object.fromEntries(s.points.map((p) => [p.period, p.value]));
    return periods.map((period) => byPeriod[period] ?? null);
  });
}

function renderChart(series) {
  const mount = document.getElementById("kpi-chart");
  mount.innerHTML = "";
  if (!series.length || typeof uPlot === "undefined") {
    return;
  }
  const periods = [...new Set(series.flatMap((s) => s.points.map((p) => p.period)))].sort();
  const xs = periods.map(periodToUnix);
  const data = [xs].concat(chartSeries(series, periods));
  chart = new uPlot(chartOpts(mount, series), data, mount);
}

function chartOpts(mount, series) {
  return {
    width: mount.clientWidth || 640,
    height: 260,
    scales: { x: { time: true } },
    axes: [
      {
        stroke: "#7b8794",
        space: 56,
        values: (_u, splits) => splits.map(formatMonthTick),
      },
      {
        stroke: "#7b8794",
        size: 80,
        grid: { stroke: "#edf2ff" },
        values: (_u, splits) => splits.map(formatBrlTick),
      },
    ],
    series: chartSeriesOpts(series),
  };
}

function chartSeriesOpts(series) {
  const strokes = ["#3b5bdb", "#0ca678", "#e8590c"];
  return [
    {
      label: "Mês",
      value: (_u, raw) => (raw == null ? "--" : formatMonthTick(raw)),
    },
    ...series.map((item, index) => ({
      label: item.name,
      stroke: strokes[index % strokes.length],
      width: 2,
      value: (_u, raw) => (raw == null ? "--" : formatBrlTick(raw)),
    })),
  ];
}

function clearListsAndChart() {
  renderRanked(rankedLeft, []);
  renderRanked(rankedRight, []);
  renderBoard(boardLeft, []);
  renderBoard(boardRight, []);
  document.getElementById("kpi-chart").innerHTML = "";
  chart = undefined;
}

function showEmpty() {
  emptyState.hidden = false;
  dashCards();
  clearListsAndChart();
}

async function loadKpis() {
  emptyState.hidden = true;
  const url = `${kpiUrl}?timeframe=${encodeURIComponent(timeframeEl.value)}`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      showEmpty();
      return;
    }
    const payload = await response.json();
    renderCards(payload.cards || []);
    renderChart(payload.series || []);
    renderRanked(rankedLeft, payload.ranked_left || []);
    renderRanked(rankedRight, payload.ranked_right || []);
    renderBoard(boardLeft, payload.leaderboard_left || []);
    renderBoard(boardRight, payload.leaderboard_right || []);
  } catch (_error) {
    showEmpty();
  }
}

applyThemeHeadings();
timeframeEl.addEventListener("change", loadKpis);
dashCards();
loadKpis();
