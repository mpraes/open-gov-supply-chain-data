function periodToUnix(period) {
  const match = /^(\d{4})-(\d{2})$/.exec(period);
  if (match === null) {
    throw new Error(`period expected YYYY-MM, got ${JSON.stringify(period)}`);
  }
  const month = Number(match[2]);
  if (month < 1 || month > 12) {
    throw new Error(`period expected YYYY-MM, got ${JSON.stringify(period)}`);
  }
  return Date.UTC(Number(match[1]), month - 1, 1) / 1000;
}

function formatMonthTick(unix) {
  const date = new Date(unix * 1000);
  const month = String(date.getUTCMonth() + 1).padStart(2, "0");
  return `${date.getUTCFullYear()}-${month}`;
}

function formatBrlTick(value) {
  const absValue = Math.abs(value);
  if (absValue >= 1_000_000_000_000) {
    return compactBrl(value / 1_000_000_000_000, "tri");
  }
  if (absValue >= 1_000_000_000) {
    return compactBrl(value / 1_000_000_000, "bi");
  }
  if (absValue >= 1_000_000) {
    return compactBrl(value / 1_000_000, "mi");
  }
  return `R$ ${formatPtGrouped(value)}`;
}

function compactBrl(scaled, suffix) {
  return `R$ ${scaled.toFixed(2).replace(".", ",")} ${suffix}`;
}

function formatPtGrouped(value) {
  const sign = value < 0 ? "-" : "";
  const [whole, frac] = Math.abs(value).toFixed(2).split(".");
  const grouped = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  return `${sign}${grouped},${frac}`;
}
