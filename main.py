import asyncio
from vaca_researcher import VacationResearcher

async def main():
    vaca_researcher = VacationResearcher()
    await vaca_researcher.start_mcpservers()
    request = '***'
    while request != 'quit':
        request = input('Where would you like to go or would you like me to suggest some places? ')
        if request != 'quit':
            response = await vaca_researcher.run(request=request)
            print(response.final_output)
        else:
            await vaca_researcher.stop_mcpservers()
            print('Thanks for using Vacation Researcher!')
            
if __name__ == '__main__':
    asyncio.run(main())
