function calc(d) {
  let r = 0;
  for (let i = 0; i < d.length; i++) {
    if (d[i].s > 1000 && d[i].c === 'RU') r += d[i].p * 0.9;
    else if (d[i].s > 500) r += d[i].p * 0.95;
    else r += d[i].p;
  }
  return r;
}
