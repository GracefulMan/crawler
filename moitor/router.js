'use strict';
const fs = require('fs');
const Router = require('koa-router');
const router = new Router();
function add_rule(router, rule) {
    for (let key in rule['routers']) {
        if (key.startsWith('GET ')) {
            let path = key.substring(4);
            router.get(path, rule['routers'][key]);
            console.log(`register URL mapping: GET ${path}`);
        } else if (key.startsWith('POST ')) {
            let path = key.substring(5);
            router.post(path, rule['routers'][key]);
            console.log(`register URL mapping: POST ${path}`);
        } else if (key.startsWith('DEL ')) {
            let path = key.substring(4);
            router.del(path, rule['routers'][key]);
            console.log(`register URL mapping: POST ${path}`);
        } else if (key.startsWith('PUT ')) {
            let path = key.substring(4);
            router.put(path, rule['routers'][key]);
            console.log(`register URL mapping: PUT ${path}`);
        } else {
            console.log(`invalid URL: ${key}`);
        }
    }
}

// Import all controllers
function add_rules(router) {
    let files = fs.readdirSync(__dirname + '/controller');
    let js_files = files.filter((f) => {
        return f.endsWith('.js');
    });
    for (let f of js_files) {
        console.log(`process controller: ${f}...`);
        let rule = require(__dirname + '/controller/' + f);
        add_rule(router, rule);
    }
}
add_rules(router);
module.exports.routers = function () {
    return router.routes();
};
