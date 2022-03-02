"use strict";

const Discord = require("discord.js");
const { Client, Intents } = require("discord.js");
const config = require("./config.json");
const fs = require("fs");
const mysql = require('mysql2/promise')
//const util = require("./src/util");

async function main() {
  //await util.init();
  const database = await mysql.createConnection(config.database);
  //create any tables needed if they don't already exist
  await database.execute("CREATE TABLE IF NOT EXISTS `server` (`guild_id` char(18) PRIMARY KEY, `server_ip` TEXT NOT NULL)")
  //util.queryDB("CREATE TABLE IF NOT EXISTS `server` (`guild_id` int PRIMARY KEY AUTO_INCREMENT , `server_ip` TEXT NOT NULL)")

  const client = new Client({
    intents: [
      'GUILDS',
      'GUILD_MESSAGES',
      'GUILD_MESSAGE_REACTIONS'
      ],
    allowedMentions: { parse: [] },
  });

  client.commands = new Discord.Collection();
  client.cooldowns = new Discord.Collection();
  const prefix = /^<@!?889197952994791434>/

  const commandFolders = fs.readdirSync("./src/commands");
  for (const folder of commandFolders) {
    const commandFiles = fs
      .readdirSync(`./src/commands/${folder}`)
      .filter((file) => file.endsWith(".js"));
    for (const file of commandFiles) {
      const command = require(`./src/commands/${folder}/${file}`);
      client.commands.set(command.name, command);
    }
  }
  const commandFiles = fs
    .readdirSync("./src/commands")
    .filter((file) => file.endsWith(".js"));
  for (const file of commandFiles) {
    const command = require(`./src/commands/${file}`);
    // set a new item in the Collection
    // with the key as the command name and the value as the exported module
    client.commands.set(command.name, command);
  }
  client.on("ready", () => {
    client.user.setPresence({
      status: "dnd",
      activities: [{ type: "WATCHING", name: 'you (prefix: @mention")' }],
    });
    console.log("I am ready!");
  });

  client.on("messageCreate", (message) => {
    if (!prefix.test(message.content) || message.author.bot) return;
    const args = message.content.replace(prefix, '').trim().split(' ');
    const commandName = args.shift().toLowerCase();
    const command =
      client.commands.get(commandName) ||
      client.commands.find(
        (cmd) => cmd.aliases && cmd.aliases.includes(commandName)
      );
    if (!command) return;

    if (command.permissions) {
      const authorPerms = message.channel.permissionsFor(message.author);
      if (!authorPerms || !authorPerms.has(command.permissions)) {
        return message.reply(
          `You do not have the required permissions for this: \`${command.permissions}\``
        );
      }
    }

    if (command.args && !args.length) {
      return message.reply(
        `Please specify arguments for this command - \`${command.usage.toString()}\``
      );
    }

    const { cooldowns } = client;

    if (!cooldowns.has(command.name)) {
      cooldowns.set(command.name, new Discord.Collection());
    }

    const now = Date.now();
    const timestamps = cooldowns.get(command.name);
    const cooldownAmount = (command.cooldown || 3) * 1000;

    if (timestamps.has(message.author.id)) {
      const expirationTime = timestamps.get(message.author.id) + cooldownAmount;

      if (now < expirationTime) {
        const timeLeft = (expirationTime - now) / 1000;
        return message.reply(
          `please wait ${timeLeft.toFixed(
            1
          )} more second(s) before reusing the \`${command.name}\` command.`
        );
      }
    }

    timestamps.set(message.author.id, now);
    setTimeout(() => timestamps.delete(message.author.id), cooldownAmount);

    try {
      command.execute(message, args, client); // Add ", database" behind client when using databases
      console.log(`Command "${command.name}" was executed by ${message.author.tag} (${message.author.id})`)
    } catch (error) {
      console.error(error);
      message.reply(
        `there was an error trying to execute that command!\n\`${error}\``
      );
    }
  });
  await client.login(config.token);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
