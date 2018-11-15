const mongoose = require('mongoose');
const express = require('express');
const app = express();
const http = require('http');
const User = require('./user.model');

app.use(express.json());

app.post('/register', async (req, res) => {
    const newUser = new User(req.body);
    await newUser.save();
    res
        .status(201)
        .json({
            message: 'Usuario creado con exito'
        });
});

app.post('/login', async (req, res) => {
    const user = await User.findOne({
        'cedula': req.body.cedula
    });
    console.log(req.body)

    if (user) {
        res
            .status(200)
            .json({
                data: {
                    huella: user.huella
                }
            })
    } else {
        res
            .status(401)
            .json({
                message: 'No se encontro un usuario con esa cedula en el sistema'
            });
    }
});



mongoose
    .connect('mongodb://localhost:27017/ujap', { useNewUrlParser: true })
    .then(() => {
        http
            .createServer(app, () => {
                console.log('Servidor iniciado en localhost:3000');
            })
            .listen(3000);
    })
    .catch(err => {
        console.log('Error al conectar a la BD');
        throw err;
    });
