function getDiscount(sum, country) {
  if (sum > 1000 && country === 'RU') return 0.9;
  if (sum > 500) return 0.95;
  return 1;
}

function calculateTotalPrice(items) {
  return items.reduce((total, item) => {
    return total + item.price * getDiscount(item.sum, item.country);
  }, 0);
}

module.exports = calculateTotalPrice;