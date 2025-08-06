import asyncio
import streamlit as st

from vaca_researcher import VacationResearcher
from messaging_common import *

@st.cache_resource
def load_research_agent():
    return VacationResearcher()

async def main():
    vaca_researcher = load_research_agent()

    st.set_page_config(page_title=UI_MAIN_TITLE, layout='wide')
    st.title(UI_MAIN_TITLE)
    st.write(UI_MAIN_HEADER)

    left_col, right_col = st.columns([1, 3])
    with left_col:
        name = st.text_input(UI_NAME_TITLE)
        cur_location = st.text_input(UI_CUR_LOCATION_TITLE)
        cur_prefs = st.text_area(UI_PREFS_TITLE)
        if st.button(UI_PREFS_BUTTON_TITLE):
            prefs_manager.set_name(name)
            prefs_manager.set_cur_location(cur_location)
            prefs_manager.set_prefs(cur_prefs)
            
    with right_col:
        request = st.text_input(UI_MAIN_PROMPT)
        submit_button, quit_button = st.columns([1, 1])
        submit_button.empty()
        quit_button.empty()
        response_area = st.empty()
        
        if submit_button.button(UI_SUBMIT_BUTTON_TITLE):
            with st.spinner(UI_IN_PROGRESS_TEXT):
                response_area.empty()
                response = await vaca_researcher.run(request)
                response_area.markdown(f'{response}')
    
        if quit_button.button(UI_QUIT_BUTTON_TITLE):
            st.write(UI_GOODBYE_TEXT)

if __name__ == "__main__":
    asyncio.run(main())
