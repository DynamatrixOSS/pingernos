const { ping } = require("minecraft-protocol");
const util = require("../../util");

module.exports = {
  name: "ping",

  aliases: ["latency", "pong"],

  description: "Get the bot and websocket latency",

  cooldown: 5,

  async execute(message, args, client) {
    const pong = await message.reply("Loading data");
    try {
      const result = await util.retry(ping, null, [{host: `example.aternos.me`}]);
      await pong.edit(
        `🏓 Latency is ${
          pong.createdTimestamp - message.createdTimestamp
        }ms.\nAPI Latency is ${Math.round(
          client.ws.ping
        )}ms\nProtocol: ${JSON.stringify(result.latency)} ms`
      );
    } catch (e) {
      return await message.reply(`Error caught: \`${e}\``);
    }
  },
};
