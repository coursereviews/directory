from directory.exceptions import DirectoryException

class Person(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __str__(self):
        return '<Person {}>'.format(self.webid)

    def __repr__(self):
        return self.__str__()
