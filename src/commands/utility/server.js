const {ping} = require('minecraft-protocol');
const Discord = require("discord.js");
const { color } = require('../../util')

module.exports = {
    name: 'status',

    args: true,

    aliases: ['s', 'status'],

    usage: '<server IP (without .aternos.me)',

    description: 'Get the server status',

    cooldown: 60,

async execute(message, args, client) {
        function removeColorsFromString (text) { // Removing minecraft colors from strings, because console can`t read it and it will look crazy.
            return text.replace(/§./g, '')
        }

        console.log(args[0])
        const ip = args[0].match(/^(\w+)(?:\.aternos\.me)?$/i)[1];

        const test = await ping({host: `${ip}.aternos.me`});

        if(test.version.name === '§4● Offline') {
            const embed = new Discord.MessageEmbed()
                .setTitle(`${ip}.aternos.me`)
                .addFields(
                    /** @type {any} */ {name: '__**Status**__', value: 'Offline', inline: true},
                    /** @type {any} */ {name: '__**Players**__', value: 'unknown', inline: true},
                    /** @type {any} */ {name: '__**Latency**__', value: JSON.stringify(test.latency), inline: true}
                )
                .setColor(color.red)
                .setFooter(`Command executed by ${message.author.tag}`)
                .setTimestamp()
            await message.reply( { embeds: [embed] } )
        } else {
            const embed = new Discord.MessageEmbed()
                .setTitle(`${ip}.aternos.me`)
                .addFields(
                    /** @type {any} */ {name: '__**Status**__', value: 'Online', inline: true},
                    /** @type {any} */ {name: '__**Players**__', value: JSON.stringify(test.players.online) + `/` + JSON.stringify(test.players.max), inline: true},
                    /** @type {any} */ {name: '__**Latency**__', value: JSON.stringify(test.latency), inline: true}
                )
                .setColor(color.green)
                .setFooter(`Command executed by ${message.author.tag}`)
                .setTimestamp()
            await message.reply({embeds: [embed]});
        }
    },
};