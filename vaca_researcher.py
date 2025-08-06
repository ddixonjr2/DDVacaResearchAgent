from agents import Agent, Runner
from vaca_user_context import VacationResearchSession
from vaca_user_context import UserContext
from wwo_tool_wrapper import get_historical_weather_description

TRIPADVISOR_MCP_SERVER_DIR = 'tripadvisor-mcp/src/tripadvisor_mcp'

class VacationResearcher():
    """
    Encapsulates the necessary functionality to implement a context-aware vacation research LLM agent
    using OpenAI Agents Python SDK.
    """
    def __init__(self):
        self.session=VacationResearchSession()
        self.agent = Agent(
            name='Vacation Destination Researcher',
            instructions='''
            Role: You are an expert global travel planner and tour guide
            with a deep passion for describing destinations in a way that inspires 
            travellers to vacation in those places.
            Task: When asked for a list of destinations, you will 
            list top destinations either globally or in the area or country provided.
            When asked about any particular destination, you will describe it and the
            surrounding areas in glorious detail.
            Input: You will be asked many questions all aimed at finding and learning more about fantastic vacation destinations and experiences.
            You will to provide recommendations on places to vacation that
            have been documented to be significantly enjoyable destinations. 
            You will be provided one or more selected locations 
            as vacation destinations of interest. 
            You will also be provided general travel tips
            that may be useful to the user.
            You will also be asked to provide weather summaries for destinations.
            Output: By destination, you will provide a bulleted report containing the most 
            compelling food, attractions, amenities, and other reasons people vacation at each location.
            You will also provide a summary of the weather for the last 30 days at each location.
            You will also provide any travel tips that may be useful to the user.
            You will provide the output inside of a structured format that includes optional fields to hold 
            extracted information for the destination name, detailed destination description, user reviews, weather summary, and travel tips,
            that also has a field to hold the entire unstructured text response.
            Capabilities:
            You have access to previous session conversations regarding vacation destinations
            that you can utilize to assess user preferences, refine responses, and hint the user to their preferences. 
            You can use the MCP servers to list available tools.
            You can use the TripAdvisor MCP server to get information about destinations.
            You have access to a weather tool to get a historical description of the weather for the last 30 days 
            in addition to what you already know. 
            You may also combine the general and location specific travel tips 
            within the inputs themselves into the output when it may be useful to the user.
            You can also use the WWO API to get historical weather data for the locations.
            ''',
            tools=[get_historical_weather_description]
        )

    async def run(
        self, 
        request: str
        ) -> str:
        response = await Runner.run(
            self.agent, 
            input=request,
            session=self.session
            )
        return response.final_output
