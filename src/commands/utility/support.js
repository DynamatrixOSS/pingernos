const Discord = require("discord.js");
const util = require("../../util");

module.exports = {
  name: "support",

  description: "Get support here",

  async execute(message, args, client) {
    const embed = new Discord.MessageEmbed()
      .setDescription(
        `[join our support server](${util.links.support}) or contact **modraxisorg@gmail.com**.`
      )
      .setColor(util.color.blue);

    await message.reply({ embeds: [embed] });
  },
};
