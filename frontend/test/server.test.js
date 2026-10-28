const test = require("node:test");
const assert = require("node:assert/strict");

const { app, formatPrice, renderMenu } = require("../server");

test("formatPrice uses rupees with Indian digit grouping", () => {
  assert.equal(formatPrice(180), "Rs 180");
  assert.equal(formatPrice(125000), "Rs 1,25,000");
});

test("renderMenu lists every item", () => {
  const html = renderMenu([{ name: "Latte", price: 170 }, { name: "Mocha", price: 210 }]);
  assert.match(html, /<li>Latte - Rs 170<\/li>/);
  assert.match(html, /<li>Mocha - Rs 210<\/li>/);
});

test("GET /health returns ok", async () => {
  const server = app.listen(0);
  const { port } = server.address();
  const res = await fetch(`http://127.0.0.1:${port}/health`);
  assert.equal(res.status, 200);
  assert.equal((await res.json()).status, "ok");
  server.close();
});
