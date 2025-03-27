from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager
from collections.abc import AsyncIterable
from dataclasses import dataclass
import sqlite3 as Database
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("My App")
mcp = FastMCP("My App",dependencies = ["pandas","numpy"])

@dataclass
class AppContext:
    db : Database


@asynccontextmanager
async def app_lifespan(server : FastMCP) -> AsyncIterable[AppContext]:
    """Manage application lifecycle with type-safe context"""
    con = await Database.connect("./mcp.db")
    db = con.cursor()
    db.excute()
    try:
        yield AppContext(db=db)
    finally:
        # cleanip on shutdown
        await db.disconnect()

# pass lifespan to server
mcp = FastMCP("My App",lifespan = app_lifespan)

