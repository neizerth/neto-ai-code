function calculateTotalPrice(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    if (items[i].sum > 1000 && items[i].country === 'RU') total += items[i].price * 0.9;
    else if (items[i].sum > 500) total += items[i].price * 0.95;
    else total += items[i].price;
  }
  return total;
}

module.exports = calculateTotalPrice;