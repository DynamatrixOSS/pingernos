const util = require("../../util");
const Discord = require("discord.js");
const {ping} = require("minecraft-protocol");


module.exports = {
    name: "setserver",

    aliases: ["set"],

    description: "Set the default server to use if no argument is provided in the status command.",

    args: true,

    usage: "<Aternos server ip>",

    cooldown: 5,

    async execute(message, args, client) {
        let ip = args[0].match(/^(\w+)(?:\.aternos\.me)?$/i);

        if (!ip) {
            await message.reply(`\`${args}\` is not a valid Aternos server IP or name.`);
            return;
        }

        ip = ip[1];


        const test = await ping({host: `${ip}.aternos.me`});
        //console.log(test)

        if (test.version.name === "⚠ Error") {
            return await message.reply(`:warning: \`${args}\` is not a known server.`);
        } else {
            await message.reply(`Checkpoint before sql`)
            if (!(await util.queryDB("SELECT server_ip FROM server WHERE guild_id = ?", [message.guild.id])).length) {
                await util.queryDB("INSERT INTO server (guild_id, server_ip) VALUES (?,?)", [message.guild.id, ip])
                await message.reply("The server has been set as default successfully.")
            } else {
                await util.queryDB("UPDATE server SET server_ip = ? WHERE guild_id = ?", [ip, message.guild.id])
                await message.reply("The server has been set as default successfully.")
            }
        }
    },
};