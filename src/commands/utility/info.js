const util = require("../../util");
const Discord = require("discord.js");

module.exports = {
    name: "info",

    aliases: ["information", "support", "invite"],

    description: "Information about Pingernos",

    async execute(message, args, client) {
        const embed = new Discord.MessageEmbed()
            .setDescription(
                `${client.user.username} is not affiliated with Aternos GmbH, but is a bot developed by \
                 [PsychOps Studios](https://psychops.tk) with the purpose of offering Aternos users a public alternative to the \
                  private Aternos bot.\n\n[[Invite]](${util.links.invite}) [[Support]](${util.links.support}) \
                   [[Github]](https://github.com/PsychOps/serverpinger) [[Aternos]](https://aternos.org/)`
            )
            .setColor(util.color.blue);

        await message.reply({ embeds: [embed] });
    },
};
