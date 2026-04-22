module.exports = (app) => {
  const router = require("express").Router();

  const productController = require("../controllers/product.controller");
  const categoryController = require("../controllers/category.controller");

  // PRODUCTS
  router.post("/products", productController.create);
  router.get("/products", productController.findAll);
  router.get("/products/:id", productController.findOne);
  router.put("/products/:id", productController.update);
  router.delete("/products/:id", productController.delete);
  router.get("/products/category/:id", productController.findByCategory);

  // CATEGORIES
  router.post("/categories", categoryController.create);
  router.get("/categories", categoryController.findAll);
  router.get("/categories/:id", categoryController.findOne);
  router.put("/categories/:id", categoryController.update);
  router.delete("/categories/:id", categoryController.delete);

  app.use("/api", router);
};