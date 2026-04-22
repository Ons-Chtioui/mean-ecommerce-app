const express = require('express');
require('dotenv').config();
const cors = require('cors');

const database = require('./src/database/db.config');

const app = express();

// middleware
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// DB connection
database.mongoose
  .connect(database.url)
  .then(() => console.log('connected to database'))
  .catch(err => console.log(err));

// routes
require('./src/api/routes/routes')(app);

// test route
app.get('/', (req, res) => {
  res.send({ message: 'Hello, World!' });
});

// server
app.listen(process.env.PORT, () => {
  console.log('Server is running on port', process.env.PORT);
});