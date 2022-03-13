const Discord = require("discord.js");
const util = require("../../util");

module.exports = {
  name: "guilds",
  aliases: ["servers"],
  description: "Shows how many guilds the bot is in.",
  
  async execute(message, args, client) {
    const embed = new Discord.MessageEmbed()
      .setDescription(`${client.user.username} is currently in ${client.guilds.cache.size} servers with a total of ${client.guilds.cache.reduce((count, guild) => count + guild.memberCount, 0)} users.`)
      .setColor(util.color.blue);

    await message.reply({ embeds: [embed] });
  },
};
