const mongoose = require('mongoose');
const userSchema = mongoose.Schema({
    'nombre': String,
    'correo': String,
    'cedula': String,
    'username': String,
    'huella': String
});

module.exports = mongoose.model('usuario', userSchema);