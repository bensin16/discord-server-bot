from interactions import ActionRow, Button, ButtonStyle, CommandContext, Client, Option, OptionType

from CoordsDB import CoordsDB
from MCManager import MCManager

from Secrets import calamity, gaiss, my_token, test_server_id

class Bot:
    def __init__(self):
        self._bot = Client(token=my_token)
        self._manager = MCManager(self)
        self._db = CoordsDB()

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
            scope = [test_server_id, calamity, gaiss]
        )
        async def buttons(ctx):
            await ctx.send("Status message (# players, server offline, etc)", components=row, ephemeral=True)

        @self._bot.component("start")
        async def start(ctx):
            res = self._manager.start_server()
            await ctx.send(res, ephemeral=True) #ephemeral=True makes it message only u back

        @self._bot.component("stop")
        async def stop(ctx):
            res = self._manager.stop_server()
            await ctx.send("endies!", ephemeral=True)

        @self._bot.command(
            name="coords",
            description="View or Add to coordinates database",
            scope=[test_server_id, calamity, gaiss],
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
                            name="dim",
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
        async def coords(ctx: CommandContext, sub_command: str, xcoord: int=0, ycoord: int=0, zcoord: int=0, desc: str="", dimension: str=""):
            if sub_command == "add":
                res = self._db.add_coord(xcoord, ycoord, zcoord, desc, dimension)
                await ctx.send(f"You added coords: {desc} at X: {xcoord} Y: {ycoord} Z: {zcoord} in the {dimension}", ephemeral=True)
            elif sub_command == "view":
                res = self._db.execute_query("select * from coords")
                outstr = ""
                for coord in res:
                    outstr += str(coord)
                await ctx.send("coords: " + outstr, ephemeral=True)


if __name__ == "__main__":
    bot = Bot()
