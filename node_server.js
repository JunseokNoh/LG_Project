var express = require('express')
var io = require('socket.io');
var app = express();
var fs = require('fs');
var path = require('path');

app.use(express.static(path.join(__dirname, '/LG_Project/webdesign')));
app.get('/',(req,res)=>{
    res.sendFile(path.join(__dirname,'/LG_Project/webdesign/index.html'))
})
app.get('/confirm',(req,res)=>{
    res.sendFile(path.join(__dirname,'/LG_Project/webdesign/confirm.html'))
})
var server = app.listen(8080,()=>{
    console.log("Express server start")
})

const socketServer = io(server);
