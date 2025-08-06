from agents import Agent, Runner, RunContextWrapper
from ta_mcp_wrapper import TripAdvisorMCPWrapper
from vaca_user_context import VacationResearchSession
from vaca_user_context import UserContext
from wwo_tool_wrapper import get_historical_weather_description


TRIPADVISOR_MCP_SERVER_DIR = 'tripadvisor-mcp/src/tripadvisor_mcp'
AGENT_NAME = 'Vacation Destination Researcher'
DEFAULT_AGENT_INSTRUCTIONS = '''
Role: You are an expert global travel planner and tour guide
with a deep passion for describing destinations in a way that inspires 
travellers to vacation in those places.
Task: When asked for suggestions, you will 
list top destinations either globally or in the area or country provided using the 
information found in the information provided about the user as much as is relevant.
When asked about any particular destination, you will describe it and the
surrounding areas in glorious detail.
When searching for destinations, you will take into consideration 
any relevant information about the user that may be useful or relevant.
Input: You will be asked many questions all aimed at finding and learning more about fantastic vacation destinations and experiences.
You will to provide recommendations on places to vacation that
have been documented to be significantly enjoyable destinations. 
You will also be provided with information regarding my name,
current location, and vacationing and travel preferences.
Output: By destination, you will provide a bulleted report containing the most 
compelling food, user reviews, attractions, amenities, and other reasons people vacation at each location.
You will always include the user's name which is provided in the request in the response.
You will also provide a summary of the weather for the last 30 days at each location from the weather tool you have access to.
You will also provide any travel tips that may be useful to the user.
Capabilities:
You can use the TripAdvisor MCP server to get information about destinations.
You have access to a weather tool to get a historical description of the weather for the last 30 days 
in addition to what you already know. 
You have access to previous session conversations regarding vacation destinations
that you can utilize to guide searches. 
'''

class VacationResearcher():
    """
    Encapsulates the necessary functionality to implement a context-aware vacation research LLM agent
    using OpenAI Agents Python SDK.
    """
    def __init__(self):
        self.tripadvisor_mcp = TripAdvisorMCPWrapper().new_mcp_server()
        self.session=VacationResearchSession()
        self.agent = Agent(
            name=AGENT_NAME,
            instructions=DEFAULT_AGENT_INSTRUCTIONS,
            mcp_servers=[self.tripadvisor_mcp],
            tools=[get_historical_weather_description]
        )

    async def start_mcpservers(self):
        try:
            await self.tripadvisor_mcp.connect()
        except Exception as e:
            print(f'Failed to start trip advisor mcp server:\n{e}')

    async def stop_mcpservers(self):
        try:
            await self.tripadvisor_mcp.cleanup()
        except Exception as e:
            print(f'Failed to stop the tripadvisor mcp server gracefully:\n{e}')

    async def run(
        self, 
        request: str,
        context: UserContext
        ) -> str:
        augmented_request = context.context_augmented_request(request)
        print(f'Running augmented request:\n{augmented_request}')
        response = await Runner().run(
            self.agent, 
            input=augmented_request,
            session=self.session
            )
        return response.final_output
