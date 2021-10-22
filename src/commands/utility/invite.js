const util = require("../../util");
const Discord = require("discord.js");

module.exports = {
  name: "invite",

  aliases: ["inv"],

  description: "Invite me to your server(s)!",

  async execute(message, args, client) {
    const embed = new Discord.MessageEmbed()
      .setDescription(
        `${client.user.username} is a Modraxis Development project. [Invite it here!](${util.links.invite})`
      )
      .setColor(util.color.blue);

    await message.reply({ embeds: [embed] });
  },
};
