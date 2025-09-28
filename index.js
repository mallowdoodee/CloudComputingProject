const express = require('express');
// const mysql = require('mysql');
const app = express();
const port = 8000
const path = require("path");

app.set('view engine', 'ejs')
app.set("views", path.join(__dirname, "views"));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// const con = mysql.createConnection({
//     host: "localhost",
//     user: "root",
//     password: "",
//     database: "mydb"
// })

// con.connect(function (err) {
//   if (err) throw err;
//   console.log("Connected!");
// });

app.get('/', (req, res) => {
    res.render("home.ejs")
})

// app.post("/signup", (req, res) => {
//   const { username, password } = req.body;
//   console.log("username: ", username);
//     if (username.length == 0) {
//         return res.render("signup")
//     }
//   const query = "INSERT INTO signup (username, password) VALUES (?, ?)";
//   con.query(query, [username, password], (err, result) => {
//     if (err) {
//       console.error("Error inserting data:", err);
//       return res.status(500).send("Database error");
//     }
//     // console.log("Inserted ID:", );
//     res.send("Signup success!");
//   });
// });

// app.get('/login', (req, res) => {
//     res.render('login')
// })

// app.post('/api/login', (req, res) => {
//     const { username, password } = req.body;
//     console.log("usrename: ", username)

//     const query = "SELECT * FROM signup WHERE username = ? AND password = ?"
//     con.query(query, [username, password], (err, result) => {
//         if (err) {
//             console.error("Error inserting data:", err);
//             return res.redirect('/login')
//         }
//         console.log("result: ", result)
//         return res.redirect('/')
//     })
// })


app.listen(port, () => {
    console.log("Server running on http://localhost:"+port)
})