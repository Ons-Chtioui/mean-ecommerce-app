const db = require("../../database/db.config");
const Category = db.categories;

// 🟢 CREATE
exports.create = async (req, res) => {
  try {
    const { name, description } = req.body;

    if (!name) {
      return res.status(400).json({
        success: false,
        message: "Category name is required"
      });
    }

    const category = new Category({
      name,
      description: description || ""
    });

    const saved = await category.save();

    return res.status(201).json({
      success: true,
      message: "Category created successfully",
      data: saved
    });

  } catch (err) {
    return res.status(500).json({
      success: false,
      message: err.message
    });
  }
};

// 📥 GET ALL
exports.findAll = async (req, res) => {
  try {
    const data = await Category.find();

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
    const data = await Category.findById(req.params.id);

    if (!data) {
      return res.status(404).json({
        success: false,
        message: "Category not found"
      });
    }

    res.status(200).json({
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
    const data = await Category.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }
    );

    if (!data) {
      return res.status(404).json({
        success: false,
        message: "Category not found"
      });
    }

    res.status(200).json({
      success: true,
      message: "Category updated successfully",
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
    const data = await Category.findByIdAndDelete(req.params.id);

    if (!data) {
      return res.status(404).json({
        success: false,
        message: "Category not found"
      });
    }

    res.status(200).json({
      success: true,
      message: "Category deleted successfully"
    });

  } catch (err) {
    res.status(500).json({
      success: false,
      message: err.message
    });
  }
};