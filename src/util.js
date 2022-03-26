
const config = require('../config.json');
const mysql = require('mysql2/promise')
const util = {};

util.retry = async (fn, thisArg, args = [], maxRetries = 5, returnValMatch = null) => {
  let err;
  for (let i = 0; i < maxRetries; i++) {
    let res;
    try {
      res = await Promise.resolve(fn.apply(thisArg, args));
    } catch (e) {
      err = e;
      continue;
    }
    if (typeof returnValMatch === 'function' && !returnValMatch(res)) {
      err = new Error('Returned value did not match requirements');
      continue;
    }
    return res;
  }
  throw err;
};

util.color = {
  blue: 0xadd8e6,
  red: 0xf04747,
  green: 0x90ee90,
  orange: 0xfaa61a,
};

util.links = {
  support: "https://discord.gg/QMhvHuGPMx",
  invite:
    "https://discord.com/api/oauth2/authorize?client_id=889197952994791434&permissions=274878286848&scope=bot",
};

module.exports = util;
