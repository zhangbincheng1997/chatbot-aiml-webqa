#!/usr/bin/python
# -*- coding: UTF-8 -*-

import shelve

DB_PATH = "resources/simple_rules.db"
AIML_PATH = "resources/save.aiml"


def save(question, answer):
    template = """<aiml version="1.0.1" encoding="UTF-8">
    {rules}
    </aiml>
    """

    category_template = """
    <category>
        <pattern>{pattern}</pattern>
        <template>
            {answer}
        </template>
    </category>
    """
    db = shelve.open(DB_PATH, "c", writeback=True)
    db[question] = answer
    db.sync()
    rules = []
    for r in db:
        rules.append(category_template.format(pattern=r, answer=db[r]))
    content = template.format(rules="\n".join(rules))
    with open(AIML_PATH, "w") as fp:
        fp.write(content)
