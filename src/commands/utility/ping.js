const {ping} = require('minecraft-protocol');

module.exports = {
    name: 'ping',

    aliases: ['latency', 'pong'],

    description: 'Get the bot and websocket latency',

    cooldown: 60,

    async execute(message, args, client) {
        const pong = await message.reply('Loading data');
        try {
            const whatthefuck = await ping({host: `example.aternos.me`});
            console.log(whatthefuck)
            await pong.edit(`🏓 Latency is ${pong.createdTimestamp - message.createdTimestamp}ms.\nAPI Latency is ${Math.round(client.ws.ping)}ms\nProtocol: ${JSON.stringify(whatthefuck.latency)} ms`);
        } catch (e) {
            return await message.reply(`Error caught: \`${e}\``);
        }
    },
};
