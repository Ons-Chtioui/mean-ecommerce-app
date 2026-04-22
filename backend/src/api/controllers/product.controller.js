const db = require("../../database/db.config");
const Product = db.products;
const Category = db.categories;

// 🟢 CREATE PRODUCT (AMÉLIORÉ)
exports.create = async (req, res) => {
  try {
    const { name, description, price, category, stock, image } = req.body;

    // validation
    if (!name || !description || !price || !category) {
      return res.status(400).json({
        success: false,
        message: "Name, description, price and category are required"
      });
    }

    // check category
    const cat = await Category.findById(category);
    if (!cat) {
      return res.status(404).json({
        success: false,
        message: "Category not found"
      });
    }

    // create product
    const product = new Product({
      name: name.trim(),
      description,
      price,
      category,
      stock: stock || 0,
      image: image || ""
    });

    const saved = await product.save();

    res.status(201).json({
      success: true,
      message: "Product created successfully",
      data: saved
    });

  } catch (err) {
    res.status(500).json({
      success: false,
      message: err.message
    });
  }
};

// 📥 GET ALL
exports.findAll = async (req, res) => {
  try {
    const data = await Product.find().populate("category");

    res.status(200).json({
      success: true,
      count: data.length,
      data
    });

  } catch (err) {
    res.status(500).json({
      success: false,
      message: err.message
    });
  }
};

// 📥 GET ONE
exports.findOne = async (req, res) => {
  try {
    const data = await Product.findById(req.params.id).populate("category");

    if (!data) {
      return res.status(404).json({
        success: false,
        message: "Product not found"
      });
    }

    res.json({
      success: true,
      data
    });

  } catch (err) {
    res.status(500).json({
      success: false,
      message: err.message
    });
  }
};

// ✏️ UPDATE
exports.update = async (req, res) => {
  try {
    const data = await Product.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }
    );

    if (!data) {
      return res.status(404).json({
        success: false,
        message: "Product not found"
      });
    }

    res.json({
      success: true,
      message: "Product updated successfully",
      data
    });

  } catch (err) {
    res.status(500).json({
      success: false,
      message: err.message
    });
  }
};

// ❌ DELETE
exports.delete = async (req, res) => {
  try {
    const data = await Product.findByIdAndDelete(req.params.id);

    if (!data) {
      return res.status(404).json({
        success: false,
        message: "Product not found"
      });
    }

    res.json({
      success: true,
      message: "Product deleted successfully"
    });

  } catch (err) {
    res.status(500).json({
      success: false,
      message: err.message
    });
  }
};

// 📂 FILTER BY CATEGORY
exports.findByCategory = async (req, res) => {
  try {
    const data = await Product.find({ category: req.params.id });

    res.json({
      success: true,
      count: data.length,
      data
    });

  } catch (err) {
    res.status(500).json({
      success: false,
      message: err.message
    });
  }
};