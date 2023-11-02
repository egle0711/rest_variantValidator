import random


class Model(object):

    def __init__(self):
        self.id = random.randrange(10000)
        self.related_models = list()
        for i in range(0, random.randrange(10)):
            rm = RelatedModel()
            rm.model = self
            self.related_models.append(rm)


class RelatedModel(Model):

    def __init__(self):
        self.id = random.randrange(10000)
