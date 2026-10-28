const express = require("express");

const API_URL = process.env.API_URL || "http://localhost:5000";

function formatPrice(rupees) {
  return `Rs ${Number(rupees).toLocaleString("en-IN")}`;
}

function renderMenu(items) {
  const rows = items.map((i) => `<li>${i.name} - ${formatPrice(i.price)}</li>`).join("");
  return `<h1>BrewCart Menu</h1><ul>${rows}</ul>`;
}

const app = express();

app.get("/health", (req, res) => res.json({ status: "ok", service: "frontend" }));

app.get("/", async (req, res) => {
  try {
    const items = await (await fetch(`${API_URL}/menu`)).json();
    res.send(renderMenu(items));
  } catch {
    res.status(502).send("Menu service unavailable");
  }
});

if (require.main === module) {
  const port = process.env.PORT || 3000;
  app.listen(port, () => console.log(`BrewCart frontend on port ${port}`));
}

module.exports = { app, formatPrice, renderMenu };
