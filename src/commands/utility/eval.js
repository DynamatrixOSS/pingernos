const config = require("../../../config.json");

module.exports = {
  name: "eval",
  aliases: ["evaluate"],
  description: "Evaluate a piece of JavaScript code",
  async execute(message, args, client) {
    if (!config.owners.includes(message.author.id))
      return message.channel.send(
        "This command is restricted to my developers."
      ); // simple

    const response = await message.reply("Evaluating...");
    let code = args.join(" ");
    let result;
    try {
      result = eval(code);
    } catch (e) {
      result = e.toString();
    }
    await response.edit(result);
  },
};
