const Discord = require("discord.js");
const util = require("../../util");

module.exports = {
  name: "guilds",
  aliases: ["guildcounter"],
  description: "Shows how many guilds the bot is in.",
  
  async execute(message, args, client) {
    const embed = new Discord.MessageEmbed()
      .setDescription(
        `${client.user.username} is currently in ${client.guilds.cache.size} servers with ${client.users.cache.size} users.`
      )
      .setColor(util.color.blue);

    await message.reply({ embeds: [embed] });
  },
};
