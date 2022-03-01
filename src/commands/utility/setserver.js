const util = require("../../util");
const Discord = require("discord.js");
const {ping} = require("minecraft-protocol");
//const { database } = require("/home/joshua/WebstormProjects/serverpinger/index.js")
const mysql = require("mysql2/promise");
const config = require("../../../config.json");

module.exports = {
    name: "setserver",

    aliases: ["set"],

    description: "Set the default server to use if no argument is provided in the status command.",

    args: true,

    usage: "<Aternos server ip>",

    cooldown: 5,

    async execute(message, args, client) {
        if(args[0].match('delete')) {
            const database = await mysql.createConnection(config.database);
            await database.execute("DELETE FROM server WHERE guild_id = ?", [message.guild.id]);
            await message.reply(`Server has been removed from the database.`);
            return;
        }

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
            const database = await mysql.createConnection(config.database);
            try {
                await database.execute("INSERT INTO server (guild_id, server_ip) VALUES (?,?) ON DUPLICATE KEY UPDATE server_ip = ?", [message.guild.id, ip, ip])
                await message.reply(`Successfully set default server to ${ip}\nYou can remove it using \`@prefix set delete\``)
            } catch (e) {
                console.log(e);
            }
        }
    },
};