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
Done = ["готовый", "весь"]
Error = ["Извините, я не совсем поняла Вас. Пожалуйста, повторите Ваш ответ ещё раз."]

ShortcutsYes = ["Да"]
ShortcutsNo = ["Нет"]
ShortcutsDone = ["Готово"]

ActionsQuick = ["Группы действующих лиц", "Варианты использования"]
Actions = ActionsQuick + ["Область доступа участников", "Завершить граф"]
ActionActors = ["группа", "действующий", "лицо"]
ActionUseCases = ["вариант", "использование"]
ActionRelations = ["область", "доступ", "участник"]

StateGreeting = State(["Здравствуйте! Меня зовут umling, я помогу Вам создать use-case UML диаграмму по Вашему продукту. Вы готовы начать?"], True, random_confirmation_shortcut(True))
StateName = State(["Для начала, как я могу к Вам обращаться?"], False, None)
StateConfirmName = State(["Ваше имя: {}, верно?"], True, random_confirmation_shortcut(None))
StateGraphName = State(["Очень приятно, {}! Как бы Вы хотели назвать Ваш новый граф?"], False, None)
StateGraphDescription = State(["А теперь придумайте описание для Вашего графа"], False, None)
StateBasicSelection = State(["С чего бы вы хотели начать заполнение диаграммы?"], False, ActionsQuick)
StateActors = State(["Какие лица участвуют в процессе? Например: ученик, учитель, директор"], False, ShortcutsDone)
StateUseCases = State(["Какие действия можно совершить? Например: выполнить задание, добавить в систему ученика"], False, ShortcutsDone)
StateRelations = State(["Определите область доступа для каждого участника процесса. Например: ученик - выполнить задание. Участники: {}. Доступные действия: {}"], False, ShortcutsDone)
StateSelection = State(["Что бы Вы хотели задать следующим шагом?"], False, Actions)
StateEditSelection = State(["StateEditSelection"], False, Actions)  # TODO not implemented
StateGraphDone = State(["StateGraphDone"], False, Actions)  # TODO not implemented

States = {sql.STATE_GREETING: StateGreeting, sql.STATE_NAME: StateName, sql.STATE_CONFIRM_NAME: StateConfirmName,
          sql.STATE_GRAPH_NAME: StateGraphName, sql.STATE_GRAPH_DESCRIPTION: StateGraphDescription,
          sql.STATE_BASIC_SELECTION: StateBasicSelection, sql.STATE_ACTORS: StateActors,
          sql.STATE_USE_CASES: StateUseCases, sql.STATE_RELATIONS: StateRelations, sql.STATE_SELECTION: StateSelection,
          sql.STATE_EDIT_SELECTION: StateEditSelection, }
