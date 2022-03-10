const { ping } = require("minecraft-protocol");
const Discord = require("discord.js");
const util = require("../../util");
const mysql = require("mysql2/promise");
const config = require("../../../config.json");

module.exports = {
  name: "status",

  aliases: ["s", "status"],

  permissions: 'MANAGE_GUILD',

  usage: "<Aternos server IP>",

  description: "Get the server status",

  cooldown: 5,

  async execute(message, args, client) {
    const data = [];
    const color = [];
    const description = [];
    function removeColorsFromString(text) {
      // Removing minecraft colors from strings, because console can`t read it and it will look crazy.
      return text.replace(/§./g, "");
    }

    //if(!args.length) {
      //await util.queryDB("SELECT server_ip FROM servers WHERE guild_id = ?", [message.guild.id])
    //}

      try {
      let ip;
      if(!args.length){ // Using this condition as you are
        const database = await mysql.createConnection(config.database);
        const response = await database.query("SELECT server_ip FROM server WHERE guild_id = ?", [message.guild.id])
        if(response[0][0] !== undefined){ // checking if we got an ip back
          ip = response[0][0]["server_ip"]
        }
      } else {
        ip = args[0].match(/^(\w+)(?:\.aternos\.me)?$/i)[1] // second match is the [name].aternos.me part
      }

      if (!ip) {
        if(args.length === 0){ // no ip
          await message.reply(
              `You didn't provide any Aternos server IP, nor is one configured for this guild.`);
        } else { // wrong ip
          await message.reply(
              `\`${args}\` is not a valid Aternos server IP or name.`
          );
        }
        return;
      }

      const result = await util.retry(ping, null, [{host: `${ip}.aternos.me`}]);


      if (result.version.name === "⚠ Error") {
        return await message.reply(
          `:warning: \`${args}\` is not a known server.`
        );
      }

      if (result.version.name === "§4● Offline") {
        const embed = new Discord.MessageEmbed()
          .setTitle(`${ip}.aternos.me`)
          //.addFields(
          //    /** @type {any} */ {name: '__**Status**__', value: 'Offline', inline: true},
          //    /** @type {any} */ {name: '__**Players**__', value: 'unknown', inline: true},
          //    /** @type {any} */ {name: '__**Latency**__', value: JSON.stringify(result.latency), inline: true}
          //)
          .setDescription(
            `We are not able to gather info from offline servers, sorry!\nProtocol Latency: ${JSON.stringify(
              result.latency
            )}\n\nIf you believe this is wrong, please [join our support server](${
              util.links.support
            }).`
          )
          .setColor(util.color.red)
          .setFooter(`Command executed by ${message.author.tag}`)
          .setTimestamp();
        await message.reply({ embeds: [embed] });
      } else {
        if (result.players.max === 0) {
          data.push(`loading...`);
          color.push(`0xfaa61a`);
        }
        if (result.players.max !== 0) {
          data.push(`online`);
          color.push(`0x90ee90`);
        }
        console.log(data + ` <- data | color -> ` + color);

        if(!result.modinfo) {
          if (result.description.text !== '') {
            description.push(removeColorsFromString(result.description.text));
          } else {
            description.push("No MOTD");
          }
        } else {
          if (result.description !== '') {
            description.push(removeColorsFromString(result.description));
          } else {
            description.push("No MOTD");
          }
        }

        const embed = new Discord.MessageEmbed()
          .setTitle(`${ip}.aternos.me`)
          .addFields(
            /** @type {any} */ {
              name: "__**Status**__",
              value: data.toString(),
              inline: true,
            },
            /** @type {any} */ {
              name: "__**Players**__",
              value:
                JSON.stringify(result.players.online) +
                `/` +
                JSON.stringify(result.players.max),
              inline: true,
            },
            /** @type {any} */ {
              name: "__**Software**__",
              value: removeColorsFromString(
                JSON.stringify(result.version.name)
              ).replace(/"/g, ""),
              inline: true,
            },
            /** @type {any} */ {
              name: "__**MOTD**__",
              value: description.toString(),
              inline: false,
            }
          )
          //.setDescription(`Server is currently **${data.toString()}**.\n\n**Players:** \`${JSON.stringify(result.players.online) + "`" + " out of " + "`" + JSON.stringify(result.players.max)}\`\n**Protocol Latency:** ${JSON.stringify(result.latency)}`)
          .setColor(`${color}`)
          .setFooter(`Command executed by ${message.author.tag}`)
          .setTimestamp();
        await message.reply({ embeds: [embed] });
      }
    } catch (e) {
      if (e && e.code === "ECONNREFUSED") {
        return await message.reply(
          `:warning: **Could not establish connection with protocol. Try again later.**`
        );
      }

      if (e.message.includes("ETIMEDOUT")) {
        return await message.reply(
          `:warning: **Protocol failed to respond, command timed out. Try again later.**`
        );
      }
      console.log(e);
      const embed = new Discord.MessageEmbed()
        .setTitle(`:warning: Fatal error :warning:`)
        .setDescription(
          `A fatal error has occurred while attempting to run this command:\n\`${e}\`\nPlease report this to my developers in the [support server](${util.links.support})`
        )
        .setColor(util.color.red)
        .setFooter(`Command executed by ${message.author.tag}`)
        .setTimestamp();
      return await message.reply({ embeds: [embed] });
    }
  },
};
