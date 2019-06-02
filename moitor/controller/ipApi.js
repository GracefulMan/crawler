'use strict';
const IpModel = require("./ipApi.js");
const getIpByLocation = async ctx =>{
    let limit = ctx.query.limit || 10;
    let page = ctx.query.page || 1;
    let location  = ctx.query.location || -1;
    let skip = (page - 1) * limit;
    let ipList = await IpModel.getIp(limit,skip,location);
    ctx.body = ipList;
    ctx.status = 200;
};
module.exports.routers = {
    'GET /ip/getIp':getIpByLocation,
};
