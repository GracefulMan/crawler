"use strict";
const Koa = require('koa');
const config = require('./config.js');
const bodyParser = require('koa-bodyparser');
const mysql = require('mysql');
const logger = require('koa-logger');
const routers = require('./router.js');
const parse = require('co-busboy');
const fs=require('fs');
const render = require('koa-ejs');
const path = require('path');
const app = new Koa();
render( app, {
    root:path.join(__dirname,'view'),
    layout:'ipServer',
    viewExt: 'ejs',
    cache: false,
    debug: true
    }
);


// const fileRouter=require('koa-router')();
// const multer = require('koa-multer');
//middlewires
// const storage = multer.diskStorage({
//     destination:function (req,file,cb) {
//         cb(null,config.fileDir1)
//     },
//     filename:function (req,file,cb) {
//         let firFormat = (file.originalname).split(".");
//         let tempFilename = Date.now()+firFormat[firFormat.length-1]+Math.random();
//         tempFilename = commonFunction.md5(tempFilename);
//         cb(null,tempFilename);
//     }
// });
// var upload = multer({storage:storage});
// fileRouter.post('/uploadAvatar',upload.single('file'),async(ctx,next)=>{
//     ctx.body=ctx.req.file.filename;
// });

//middlewires
app.use(
    bodyParser({
        multipart: true
    })
);
app.use(async (ctx, next) => {
    // the body isn't multipart, so busboy can't parse it
    if (!!ctx.request.is('multipart/*')) {
        var parts = parse(ctx);
        var part;
        while ((part = await parts())) {
            if (part.length) {
                // arrays are busboy fields
                console.log('key: ' + part[0]);
                console.log('value: ' + part[1]);
            } else {
                // otherwise, it's a stream
                ctx.req.part = part;
                console.log(part);
                await next(ctx);
                return;
            }
        }
        console.log('and we are done parsing the form!');
    }
    await next();
});
app.use(routers.routers());
app.use(logger());
app.listen(config.port);
console.log(`connect to database ${config.database.DATABASE} at port ${config.database.PORT}`);
console.log(`listening on port ${config.port}...`);


//create mysql connection pool
const pool = mysql.createPool(
    {
        host:config.database.HOST,
        user:config.database.USERNAME,
        password:config.database.PASSWORD,
        database:config.database.DATABASE
    }
);
exports.query =(sql,values)=>{
    return new Promise((resolve , reject) =>{
        pool.getConnection( (err,connection)=>{
            if(err) reject(err);
            else {
                connection.query(sql,values,(err,rows)=>{
                    if(err) reject(err);
                    else {
                        resolve(rows);
                    }
                    connection.release();
                })
            }
        })
    })
};

