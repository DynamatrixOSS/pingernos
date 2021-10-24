const { ping } = require("minecraft-protocol");
const Discord = require("discord.js");
const util = require("../../util");

module.exports = {
  name: "status",

  args: true,

  aliases: ["s", "status"],

  usage: "<Aternos server IP>",

  description: "Get the server status",

  cooldown: 60,

  async execute(message, args, client) {
    const data = [];
    const color = [];
    const description = [];
    function removeColorsFromString(text) {
      // Removing minecraft colors from strings, because console can`t read it and it will look crazy.
      return text.replace(/§./g, "");
    }

    try {
      let ip = args[0].match(/^(\w+)(?:\.aternos\.me)?$/i);

      if (!ip) {
        await message.reply(
          `\`${args}\` is not a valid Aternos server IP or name.`
        );
        return;
      }

      ip = ip[1];

      const test = await ping({ host: `${ip}.aternos.me` });

      if (test.description.text === "§4Server not found.") {
        return await message.reply(
          `:warning: \`${args}\` is not a known server.`
        );
      }

      if (test.version.name === "§4● Offline") {
        const embed = new Discord.MessageEmbed()
          .setTitle(`${ip}.aternos.me`)
          //.addFields(
          //    /** @type {any} */ {name: '__**Status**__', value: 'Offline', inline: true},
          //    /** @type {any} */ {name: '__**Players**__', value: 'unknown', inline: true},
          //    /** @type {any} */ {name: '__**Latency**__', value: JSON.stringify(test.latency), inline: true}
          //)
          .setDescription(
            `We are not able to gather info from offline servers, sorry!\nProtocol Latency: ${JSON.stringify(
              test.latency
            )}\n\nIf you believe this is wrong, please [join our support server](${
              util.links.support
            }).`
          )
          .setColor(util.color.red)
          .setFooter(`Command executed by ${message.author.tag}`)
          .setTimestamp();
        await message.reply({ embeds: [embed] });
      } else {
        if (test.players.max === 0) {
          data.push(`loading...`);
          color.push(`0xfaa61a`);
        }
        if (test.players.max !== 0) {
          data.push(`online`);
          color.push(`0x90ee90`);
        }
        console.log(data + ` <- data | color -> ` + color);

        if (test.description.text !== '') {
          description.push(removeColorsFromString(JSON.stringify(test.description.text)).replace(/"/g, ""));
        } else {
          description.push("No MOTD");
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
                JSON.stringify(test.players.online) +
                `/` +
                JSON.stringify(test.players.max),
              inline: true,
            },
            /** @type {any} */ {
              name: "__**Software**__",
              value: removeColorsFromString(
                JSON.stringify(test.version.name)
              ).replace(/"/g, ""),
              inline: true,
            },
            /** @type {any} */ {
              name: "__**MOTD**__",
              value: description.toString(),
              inline: false,
            }
          )
          //.setDescription(`Server is currently **${data.toString()}**.\n\n**Players:** \`${JSON.stringify(test.players.online) + "`" + " out of " + "`" + JSON.stringify(test.players.max)}\`\n**Protocol Latency:** ${JSON.stringify(test.latency)}`)
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
