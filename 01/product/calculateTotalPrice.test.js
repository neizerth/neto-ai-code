const calculateTotalPrice = require('./calculateTotalPrice');

describe('calculateTotalPrice', () => {
  test('calculateTotalPrice should return 0 for empty array', () => {
    expect(calculateTotalPrice([])).toBe(0);
  });

  test('calculateTotalPrice should apply 10% discount for items with sum > 1000 and country RU', () => {
    const data = [
      { sum: 1500, country: 'RU', price: 100 },
      { sum: 800, country: 'RU', price: 100 },
      { sum: 1200, country: 'US', price: 100 }
    ];
    expect(calculateTotalPrice(data)).toBe(100 * 0.9 + 100 * 0.9 + 100);
  });

  test('calculateTotalPrice should apply 5% discount for items with sum > 500', () => {
    const data = [
      { sum: 600, country: 'US', price: 100 },
      { sum: 400, country: 'RU', price: 100 }
    ];
    expect(calculateTotalPrice(data)).toBe(100 * 0.95 + 100);
  });

  test('calculateTotalPrice should not apply discount for items with sum <= 500', () => {
    const data = [
      { sum: 500, country: 'RU', price: 100 },
      { sum: 400, country: 'US', price: 100 }
    ];
    expect(calculateTotalPrice(data)).toBe(200);
  });

  test('calculateTotalPrice should correctly calculate total price with mixed conditions', () => {
    const data = [
      { sum: 1200, country: 'RU', price: 200 },
      { sum: 700, country: 'US', price: 150 },
      { sum: 300, country: 'RU', price: 100 }
    ];
    expect(calculateTotalPrice(data)).toBe(200 * 0.9 + 150 * 0.95 + 100);
  });
});