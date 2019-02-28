#!/usr/bin/env python3

# Copyright (c) 2019 Ivan Semkin.
#
# This file is part of umling
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
This is the chat database for umling.
"""

import random
from umling.api import sql

class State:
    responses = None
    requiresConfirmation = None
    shortcuts = None

    def __init__(self, responses, requires_confirmation, shortcuts):
        self.responses = responses
        self.requiresConfirmation = requires_confirmation
        self.shortcuts = shortcuts


def random_confirmation_shortcut(is_positive):
    if is_positive is None:
        return [random.choice(ShortcutsYes), random.choice(ShortcutsNo)]
    elif is_positive:
        return [random.choice(ShortcutsYes)]
    elif not is_positive:
        return [random.choice(ShortcutsNo)]


Positives = ["да", "конечно", "подтвердить", "согласный", "верно", "ок", "ok", "ага", "угу"]
Negatives = ["нет", "неа"]
Error = ["Извините, я не совсем поняла Вас. Пожалуйста, повторите Ваш ответ ещё раз."]

ShortcutsYes = ["Да"]
ShortcutsNo = ["Нет"]

Actions = ["Группы действующих лиц", "Варианты использования"]
ActionActors = ["группа", "действующий", "лицо"]
ActionUseCases = ["вариант", "использование"]

StateGreeting = State(["Здравствуйте! Меня зовут umling, я помогу Вам создать use-case UML диаграмму по Вашему продукту. Вы готовы начать?"], True, random_confirmation_shortcut(True))
StateName = State(["Для начала, как я могу к Вам обращаться?"], False, None)
StateConfirmName = State(["Ваше имя: {}, верно?"], True, random_confirmation_shortcut(None))
StateBasicSelection = State(["Очень приятно, {}! С чего бы вы хотели начать заполнение диаграммы?"], False, Actions)
StateActors = State(["StateActors"], False, None)
StateUseCases = State(["StateUseCases"], False, None)
StateRelations = State(["StateRelations"], False, None)

StateEditSelection = State([], False, Actions)

States = {sql.STATE_GREETING: StateGreeting, sql.STATE_NAME: StateName, sql.STATE_CONFIRM_NAME: StateConfirmName,
          sql.STATE_BASIC_SELECTION: StateBasicSelection, sql.STATE_ACTORS: StateActors,
          sql.STATE_USE_CASES: StateUseCases, sql.STATE_RELATIONS: StateRelations,
          sql.STATE_EDIT_SELECTION: StateEditSelection, }
