const { prefix } = require('../../../config.json');
const Discord = require('discord.js');
const { color } = require('../../util');

module.exports = {
    name: 'help',

    description: 'List all of my commands or info about a specific command.',

    usage: '[command]',

    cooldown: 3,

    async execute(message, args, client) {
        const data = [];
        const { commands } = message.client;

        if (!args.length) {
            //data.push('Here\'s a list of all my commands:');
            data.push( "`" + commands.map(command => command.name).join('`, `') + "`");
            //data.push(`\nYou can send \`${prefix}help [command name]\` to get info on a specific command!`);

            const embed = new Discord.MessageEmbed()
                .setTitle(`${client.user.username} commands | Prefix ${prefix}`)
                .setDescription(data.toString())
                .setTimestamp()
                .setFooter(`Command executed by ${message.author.tag}`)
                .setColor(color.blue)
            message.channel.send({ embeds: [embed] })// {split: true})

        } else {
            const name = args[0].toLowerCase();
            const command = commands.get(name) || commands.find(c => c.aliases && c.aliases.includes(name));

            if (!command) {
                return message.reply('that\'s not a valid command!');
            }

            //data.push(`**Name:** ${command.name} \n`);

            if (command.aliases) data.push(`**Aliases:** ${command.aliases.join(', ')} \n`);
            if (command.description) data.push(`**Description:** ${command.description} \n`);
            if (command.usage) data.push(`**Usage:** \`${prefix}${command.name} ${command.usage} \` \n`);
            if (command.permissions) data.push(`**Required permissions:** ${command.permissions} \n`)

            if (command.cooldown) data.push(`**Cooldown:** ${command.cooldown || 0} second(s)`);

            const embed = new Discord.MessageEmbed()
                .setTitle(`Help for ${command.name} | Prefix ${prefix}`)
                .setDescription(data.toString().replace(/[,]/g, ''))
                .setTimestamp()
                .setFooter(`Command executed by ${message.author.tag}`)
                .setColor(color.blue)

            message.channel.send({ embeds: [embed] }, { split: true });
        }
    },
};