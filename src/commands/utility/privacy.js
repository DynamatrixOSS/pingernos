const Discord = require("discord.js");
const util = require("../../util");

module.exports = {
  name: "privacy",

  aliases: ["policy", "pp"],

  description: "See our privacy policy.",

  async execute(message, args, client) {
    const embed = new Discord.MessageEmbed()
      .setDescription(
        `${client.user.username} saves a minimal amount of data to allow for its functionality. Full information about what is collected can be found on [W.I.P. bear with us]. For any concerns, Mail to miataboymx@gmail.com.`
      )
      .setColor(util.color.blue);

    await message.reply({ embeds: [embed] });
  },
};
