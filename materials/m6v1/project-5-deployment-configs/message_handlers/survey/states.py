from telebot import State
from telebot.handler_backends import StatesGroup


class SurveyStates(StatesGroup):
    full_name = State()
    user_email = State()
    email_newsletter = State()


all_survey_states = SurveyStates().state_list
