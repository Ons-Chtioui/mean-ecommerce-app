module.exports = mongoose => {
  const Schema = mongoose.Schema;

  const CategorySchema = new Schema(
    {
      name: {
        type: String,
        required: true,
        unique: true,
        trim: true,
        minlength: 2,
        maxlength: 50
      },

      description: {
        type: String,
        default: "",
        trim: true
      }
    },
    {
      timestamps: true
    }
  );

  // 🔄 format JSON propre pour Angular
  CategorySchema.method("toJSON", function () {
    const { __v, _id, ...object } = this.toObject();
    object.id = _id;
    return object;
  });

  return mongoose.model("Category", CategorySchema);
};