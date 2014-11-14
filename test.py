class OurClass:

    def __init__(self, a):
        self.__OurAtt = a

    def _OurAtt(self):
        return self.__OurAtt

    def _OurAtt_setter(self, val):
        if val < 0:
            self.__OurAtt = 0
        elif val > 1000:
            self.__OurAtt = 1000
        else:
            self.__OurAtt = val

    att = property(_OurAtt, _OurAtt_setter, doc='LOL')


x = OurClass(2000)
x.att(2)