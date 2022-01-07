const Discord = require("discord.js");
const config = require("../../../config.json");

module.exports = {
  name: "guilds",
  aliases: ["guildcounter"],
  description: "Shows how many guilds the bot is in.",
  
  async execute(message, args, client) {
    const embed = new Discord.MessageEmbed()
      .setDescription(
        `${client.user.username} is currently in ${client.guilds.cache.size} servers`
      )
      .setColor(util.color.blue);

    await message.reply({ embeds: [embed] });
  },
};
