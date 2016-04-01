# -*- coding: utf-8 -*-

from directory.search import Search


def search(**kwargs):
    return Search(**kwargs).results()
