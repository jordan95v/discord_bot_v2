HELP: tuple[dict[str, str], ...] = (
    dict(
        name="!ask `<text>`",
        value="Ask something to ChatGPT.",
    ),
    dict(
        name="!code `<langage> <text>`",
        value="Ask ChatGPT to code, **langage** is the for exemple python or c.",
    ),
    dict(
        name="!generate `<n>` `<prompt>`",
        value="Make ChatGPT generate `n` images.",
    ),
    dict(
        name="!del `<n>`",
        value="Delete **n** messages from the channel.",
    ),
    dict(
        name="!say `<text>`",
        value="Make the bot say something.",
    ),
    dict(
        name="!rand `<n>`",
        value="Make the bot rand a number up to **n**.",
    ),
    dict(
        name="!question `<question>`",
        value="Make the bot randomly answer a question.",
    ),
    dict(
        name="!top `<sub>` `<n>`",
        value="Scrape **n** top posts content from a subreddit **sub**.",
    ),
    dict(
        name="!hot `<sub>` `<n>`",
        value="Scrape **n** trending content from a subreddit **sub**.",
    ),
)
