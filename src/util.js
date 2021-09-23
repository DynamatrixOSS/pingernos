const util = {};

util.toTitleCase = (s) => {
    return s.toLowerCase().replace(/^(\w)|\s(\w)/g, c => c.toUpperCase());
}

/**
 * Converts a role mention (<@&roleId>) or role id to a role id
 * @param {String|module:"discord.js".Snowflake}  mention role mention (<@&roleId>) or role id
 * @return {module:"discord.js".Snowflake|null}   role id or null
 */
util.roleMentionToId = (mention) => {
    if (/^<@&\d+>$/.test(mention)) {
        return /** @type {module:"discord.js".Snowflake|null} */ mention.match(/^<@&?(\d+)>$/)[1];
    }
    else if(/^\d+$/.test(mention)) {
        return mention;
    }
    else {
        return null;
    }
};

util.color ={
    blue: 0xADD8E6,
    red: 0xf04747,
    green: 0x90ee90
}

util.links ={
    support: 'https://discord.gg/QMhvHuGPMx',
    invite: 'https://discord.com/api/oauth2/authorize?client_id=889197952994791434&permissions=274878286848&scope=bot'
}

util.escapeFormatting = (string) => {
    let currentOffset = 0;
    string = string.replace(/(.*?)(https?:\/\/[^\s\n]+)/g, (match, before, url) => {
        let res = before.replace(/([*_~`])/g,'\\$1') + url;
        currentOffset += res.length;
        return res;
    });
    return string.substr(0, currentOffset) +
        string.substr(currentOffset).replace(/([*_~`])/g,'\\$1');
};

util.userMentionToId = (mention) => {
    if (/^<@!?\d+>$/.test(mention)) {
        return /** @type {Snowflake|null} */ mention.match(/^<@!?(\d+)>$/)[1];
    }
    else if(/^\d+$/.test(mention)) {
        return mention;
    }
    else {
        return null;
    }
};

module.exports = util;