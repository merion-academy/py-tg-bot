from telebot import State
from telebot.handler_backends import StatesGroup


class ProgrammingSurveyStates(StatesGroup):
    full_name = State()
    favourite_language = State()
    experience_years = State()
    freelance = State()


all_programming_survey_states = ProgrammingSurveyStates().state_list
