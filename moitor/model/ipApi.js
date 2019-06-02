'use strict';
const connection = require(__dirname+"/index");

const getIp =(limit,skip,location) =>{
    let _sql = `SELECT * FROM ip_information WHERE (location=${location} or ${location}=-1) ORDER BY updated DESC LIMIT ${skip},${limit};`;
    return connection.query(_sql)
};

module.exports={
    getIp,
};