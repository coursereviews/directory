# -*- coding: utf-8 -*-

from directory.search import Search

def search(query, **kwargs):
    return Search(query, **kwargs).prepare().get_results()
