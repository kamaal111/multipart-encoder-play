import express from "express";

const app = express();
const port = 3000;

app.use(express.json());

app.post("/file", (req, res) => {
  console.log("req.body", req.body);
  res.json({ details: "OK" });
});

app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});
