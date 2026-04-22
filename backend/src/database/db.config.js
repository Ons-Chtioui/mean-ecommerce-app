const config = require("../config/config");
const mongoose = require("mongoose");

const db = {};

// 🔧 Promises globales
mongoose.Promise = global.Promise;

// ⚙️ config mongoose (bonne pratique)
mongoose.set("strictQuery", false);

// =========================
// 🔌 CONNECTION
// =========================
db.mongoose = mongoose;
db.url = config.DB_URL;

// =========================
// 📦 MODELS
// =========================
db.products = require("../api/models/product.model")(mongoose);
db.categories = require("../api/models/category.model")(mongoose);

module.exports = db;