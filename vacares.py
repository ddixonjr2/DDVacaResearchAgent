import asyncio
import streamlit as st

from vaca_researcher import VacationResearcher
from vaca_user_context import UserContext
from prefs_manager import PrefsManager, KEY_NAME, KEY_CURRENT_LOCATION, KEY_PREFERENCES
from messaging_common import *

@st.cache_resource
def load_research_agent():
    return VacationResearcher()

@st.cache_resource
def load_prefs_manager():
    prefs_manager = PrefsManager()
    prefs_manager.load_user_context()
    return prefs_manager

async def main():
    try:
        prefs_manager = load_prefs_manager()
        vaca_researcher = load_research_agent()
        await vaca_researcher.start_mcpservers()
    except Exception as e:
        st.error(f'Failed to initialize the vacation researcher agent:\n{e}')
        st.stop()
        raise EOFError(f'Failed to initialize in main()\n{e}')

    st.set_page_config(page_title=UI_MAIN_TITLE, layout='wide')
    st.title(UI_MAIN_TITLE)
    st.write(UI_MAIN_HEADER)

    left_col, right_col = st.columns([1, 3])
    with left_col:
        prefs_name = prefs_manager.user_context.name or ''
        name = st.text_input(
            UI_NAME_TITLE, 
            value=prefs_name, 
            placeholder=UI_NAME_PLACEHOLDER
            )

        prefs_cur_location = prefs_manager.user_context.current_location or ''
        cur_location = st.text_input(
            UI_CUR_LOCATION_TITLE, 
            value=prefs_cur_location,
            placeholder=UI_CUR_LOCATION_PLACEHOLDER
            )

        prefs_preferences = prefs_manager.user_context.preferences or ''
        prefs_display_string = ''
        for pref in prefs_preferences:
            prefs_display_string += f'{pref}\n'

        cur_prefs = st.text_area(
            UI_PREFS_TITLE,
            value=prefs_display_string,
            placeholder=UI_PREFS_PLACEHOLDER
            )

        if st.button(UI_PREFS_BUTTON_TITLE):
            prefs_manager.save_user_context(
                name=name,
                current_location=cur_location,
                preferences=cur_prefs.splitlines()
            )
            prefs_manager.load_user_context()
            
    with right_col:
        request = st.text_input(UI_MAIN_PROMPT)
        submit_button, quit_button = st.columns([1, 1])
        submit_button.empty()
        quit_button.empty()
        response_area = st.empty()
        
        if submit_button.button(UI_SUBMIT_BUTTON_TITLE):
            with st.spinner(UI_IN_PROGRESS_TEXT):
                response_area.empty()
                response = await vaca_researcher.run(request=request, context=prefs_manager.user_context)
                response_area.markdown(f'{response}')
    
        if quit_button.button(UI_QUIT_BUTTON_TITLE):
            await vaca_researcher.stop_mcpservers()
            st.write(UI_GOODBYE_TEXT)
            st.stop()
            raise EOFError('User quit the application')
        
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except EOFError:
        print('Ending session')
        loop.close()
    except Exception as e:
        print(f'Sorry, something unexpected happened.\n{e}\nPlease restart and try again.')