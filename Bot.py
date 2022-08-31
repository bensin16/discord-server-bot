from interactions import ActionRow, Button, ButtonStyle, CommandContext, Client, Option, OptionType

from MCManager import MCManager

from Secrets import my_token, test_server_id

import sqlite3

class Bot:
    def __init__(self):
        self._bot = Client(token=my_token)
        self._manager = MCManager()

        self._SetupCommands()
        self._bot.start()

    def _SetupCommands(self):
        start_button = Button(
            style=ButtonStyle.PRIMARY,
            label="Start Server",
            custom_id="start",
        )

        stop_button = Button(
            style=ButtonStyle.DANGER,
            label="Stop Server",
            custom_id="stop",
        )

        row = ActionRow(
            components=[start_button, stop_button]
        )

        @self._bot.command(
            name="buttons",
            description="Spawns start and stop buttons",
            scope = test_server_id,
        )
        async def buttons(ctx):
            await ctx.send("Status message (# players, server offline, etc)", components=row)

        @self._bot.component("start")
        async def button_response(ctx):
            res = self._manager.StartServer()
            await ctx.send(res, ephemeral=True) #ephemeral=True makes it only message u back

        @self._bot.component("stop")
        async def button_response(ctx):
            await ctx.send("stop_clicked")

        @self._bot.command(
            name="coords",
            description="View or Add to coordinates database",
            scope=test_server_id,
            options=[
                Option(
                    name="add",
                    description="Add coords to database",
                    type=OptionType.SUB_COMMAND,
                    options=[
                        Option(
                            name="xcoord",
                            description="x coordinate to save",
                            type=OptionType.INTEGER,
                            required=True
                        ),
                        Option(
                            name="ycoord",
                            description="y coordinate to save",
                            type=OptionType.INTEGER,
                            required=True
                        ),
                        Option(
                            name="zcoord",
                            description="z coordinate to save",
                            type=OptionType.INTEGER,
                            required=True
                        ),
                        Option(
                            name="desc",
                            description="what are the coords for? e.g. joe's house, stronghold, skeleton spawner, etc",
                            type=OptionType.STRING,
                            required=True
                        ),
                        Option(
                            name="dimension",
                            description="what dimension is this in? Can be Overworld, Nether, or End",
                            type=OptionType.STRING,
                            required=True
                        ),
                    ],
                ),
                Option(
                    name="view",
                    description="View coords in database",
                    type=OptionType.SUB_COMMAND,
                ),
            ],
        )
        async def coords(ctx: CommandContext, sub_command: str, xcoord: int=0, ycoord: int=0, zcoord: int=0, description: str="", dimension: str=""):
            if sub_command == "add":
                await ctx.send(f"You selected the Add sub command and put in {description} at X: {xcoord} Y: {ycoord} Z: {zcoord} in the {dimension}")
            elif sub_command == "view":
                await ctx.send(f"You selected the View sub command")


if __name__ == "__main__":
    bot = Bot()
