const Discord = require("discord.js");
const util = require("../../util");

module.exports = {
  name: "privacy",

  aliases: ["policy", "pp"],

  description: "See our privacy policy.",

  async execute(message, args, client) {
    const embed = new Discord.MessageEmbed()
      .setDescription(
        `${client.user.username} saves a minimal amount of data to allow for its functionality. Full information about what is collected can be found on [our website](https://psychops.tk/privacy.php#collected). For any concerns, [join our support server](${util.links.support}).`
      )
      .setColor(util.color.blue);

    await message.reply({ embeds: [embed] });
  },
};
