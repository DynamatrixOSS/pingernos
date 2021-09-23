const {ping} = require('minecraft-protocol');
const Discord = require("discord.js");
const util = require('../../util')

module.exports = {
    name: 'status',

    args: true,

    aliases: ['s', 'status'],

    usage: '<Aternos server IP>',

    description: 'Get the server status',

    cooldown: 60,

async execute(message, args, client) {
        const data = [];
        function removeColorsFromString (text) { // Removing minecraft colors from strings, because console can`t read it and it will look crazy.
            return text.replace(/§./g, '')
        }

        try {
            const ip = args[0].match(/^(\w+)(?:\.aternos\.me)?$/i)[1];

            const test = await ping({host: `${ip}.aternos.me`});

            if (test.description.text === '§4Server not found.') {
                return await message.reply(`:warning: \`${args}\` is not a known server.`)
            }

            if (test.version.name === '§4● Offline') {
                const embed = new Discord.MessageEmbed()
                    .setTitle(`${ip}.aternos.me`)
                    .addFields(
                        /** @type {any} */ {name: '__**Status**__', value: 'Offline', inline: true},
                        /** @type {any} */ {name: '__**Players**__', value: 'unknown', inline: true},
                        /** @type {any} */ {name: '__**Latency**__', value: JSON.stringify(test.latency), inline: true}
                    )
                    .setColor(util.color.red)
                    .setFooter(`Command executed by ${message.author.tag}`)
                    .setTimestamp()
                await message.reply({embeds: [embed]})
            } else {
                if (test.players.max === 0) data.push(`Loading...`)
                if (test.players.max !== 0) data.push(`Online`)
                console.log(data)

                const embed = new Discord.MessageEmbed()
                    .setTitle(`${ip}.aternos.me`)
                    .addFields(
                        /** @type {any} */ {name: '__**Status**__', value: data.toString(), inline: true},
                        /** @type {any} */ {
                            name: '__**Players**__',
                            value: JSON.stringify(test.players.online) + `/` + JSON.stringify(test.players.max),
                            inline: true
                        },
                        /** @type {any} */ {name: '__**Latency**__', value: JSON.stringify(test.latency), inline: true}
                    )
                    .setColor(util.color.green)
                    .setFooter(`Command executed by ${message.author.tag}`)
                    .setTimestamp()
                await message.reply({embeds: [embed]});
            }
        } catch (e) {
            if (e instanceof TypeError) {
                return message.reply(`Make sure \`${args}\` is a valid Aternos server IP. If it is, report this to my developers. (\`ping support\`)`)
            }
            const embed = new Discord.MessageEmbed()
                .setTitle(`:warning: Fatal error :warning:`)
                .setDescription(`A fatal error has occurred while attempting to run this command:\n\`${e}\`\nPlease report this to my developers in the [support server](${util.links.support})`)
                .setColor(util.color.red)
                .setFooter(`Command executed by ${message.author.tag}`)
                .setTimestamp()
            return await message.reply( { embeds: [embed] } )
        }
    },
};