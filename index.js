"use strict";

const Discord = require("discord.js");
const { Client, Intents } = require("discord.js");
const config = require("./config.json");
const fs = require("fs");
const DEL = require("@zerotwobot/del.js");
const del = new DEL(config.DELtoken, "889197952994791434");
//const mysql = require('mysql2/promise')

async function main() {
  //const database = await mysql.createConnection(config.database);
  //create any tables needed if they don't already exist
  //await database.execute("CREATE TABLE IF NOT EXISTS `example` (`id` int PRIMARY KEY AUTO_INCREMENT , `content` TEXT NOT NULL)")

  const client = new Client({
    intents: [
      Intents.FLAGS.GUILDS,
      Intents.FLAGS.GUILD_MESSAGES,
      Intents.FLAGS.GUILD_MEMBERS,
    ],
    allowedMentions: { parse: [] },
  });

  client.commands = new Discord.Collection();
  client.cooldowns = new Discord.Collection();
  const prefix = `<@889197952994791434>`

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
      activities: [{ type: "WATCHING", name: 'you (prefix "ping ")' }],
    });
    console.log("I am ready!");
    del.post(client.guilds.cache.size, 0);
    setInterval(() => {
      del.post(client.guilds.cache.size, 0); // You will probably need to change this.
    }, 600000);
  });

  client.on("messageCreate", (message) => {
    if (!prefix.test(message.content) || message.author.bot) return;
    const args = message.content.slice(prefix.length).trim().split(/ +/);
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

      timestamps.set(message.author.id, now);
      setTimeout(() => timestamps.delete(message.author.id), cooldownAmount);
    }

    try {
      command.execute(message, args, client); // Add ", database" behind client when using databases
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
