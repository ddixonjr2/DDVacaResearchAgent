
import os
from agents.mcp import MCPServerStdio

TRIPADVISOR_MCP_SERVER_DIR = 'tripadvisor-mcp/src/tripadvisor_mcp'

class TripAdvisorMCPWrapper():
    def __init__(self, ta_lib_dir: str=TRIPADVISOR_MCP_SERVER_DIR):
        self.ta_lib_dir = ta_lib_dir

    def new_mcp_server(self):
        fullpath = os.path.join(os.path.dirname(os.getcwd()), self.ta_lib_dir)
        print(f'Using {fullpath} for the location of the tripadvisor mcp server.')
        return MCPServerStdio(
            params={
                'command': 'uv',
                'args': [
                    '--directory',
                    fullpath,
                    'run',
                    'main.py'
                ]
            }
        )
