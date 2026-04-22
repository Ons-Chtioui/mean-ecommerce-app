module.exports = mongoose => {
  const Schema = mongoose.Schema;

  const ProductSchema = new Schema(
    {
      name: {
        type: String,
        required: true,
        trim: true,
        minlength: 2,
        maxlength: 100
      },

      description: {
        type: String,
        required: true,
        trim: true
      },

      price: {
        type: Number,
        required: true,
        min: 0
      },

      image: {
        type: String,
        default: ""
      },

      category: {
        type: Schema.Types.ObjectId,
        ref: "Category",
        required: true
      },

      stock: {
        type: Number,
        default: 0,
        min: 0
      },

      published: {
        type: Boolean,
        default: true
      },

      rating: {
        type: Number,
        default: 0,
        min: 0,
        max: 5
      }
    },
    {
      timestamps: true
    }
  );

  // 🔄 format JSON propre pour Angular
  ProductSchema.method("toJSON", function () {
    const { __v, _id, ...object } = this.toObject();
    object.id = _id;
    return object;
  });

  return mongoose.model("Product", ProductSchema);
};