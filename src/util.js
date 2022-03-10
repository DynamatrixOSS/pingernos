
const config = require('../config.json');
const mysql = require('mysql2/promise')
const util = {};

util.toTitleCase = (s) => {
  return s.toLowerCase().replace(/^(\w)|\s(\w)/g, (c) => c.toUpperCase());
};

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

util.queryDB = (statement, args) => {
  return new Promise((resolve, reject) => {
    console.log(`promise not succeeded`)
    connection.query(statement, args, (error, result) => {
      if(error) {
        reject(error);
      }
      else {
        resolve(result);
      }
    });
  });
}


/**
 * Converts a role mention (<@&roleId>) or role id to a role id
 * @param {String|module:"discord.js".Snowflake}  mention role mention (<@&roleId>) or role id
 * @return {module:"discord.js".Snowflake|null}   role id or null
 */
util.roleMentionToId = (mention) => {
  if (/^<@&\d+>$/.test(mention)) {
    return /** @type {module:"discord.js".Snowflake|null} */ mention.match(
      /^<@&?(\d+)>$/
    )[1];
  } else if (/^\d+$/.test(mention)) {
    return mention;
  } else {
    return null;
  }
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

let connection;
util.init = async() => {
  connection = await mysql.createConnection(config.database);
};

util.escapeFormatting = (string) => {
  let currentOffset = 0;
  string = string.replace(
    /(.*?)(https?:\/\/[^\s\n]+)/g,
    (match, before, url) => {
      let res = before.replace(/([*_~`])/g, "\\$1") + url;
      currentOffset += res.length;
      return res;
    }
  );
  return (
    string.substr(0, currentOffset) +
    string.substr(currentOffset).replace(/([*_~`])/g, "\\$1")
  );
};

util.userMentionToId = (mention) => {
  if (/^<@!?\d+>$/.test(mention)) {
    return /** @type {Snowflake|null} */ mention.match(/^<@!?(\d+)>$/)[1];
  } else if (/^\d+$/.test(mention)) {
    return mention;
  } else {
    return null;
  }
};

module.exports = util;
