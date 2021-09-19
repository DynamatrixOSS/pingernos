const {ping} = require('minecraft-protocol');

module.exports = {
    name: 'status',

    aliases: ['s', 'status'],

    description: 'Get the server status',

    cooldown: 60,

    async execute(message, args, client) {
        console.log(await ping({host: 'MinecraftGolden.aternos.me'}));
    },
};