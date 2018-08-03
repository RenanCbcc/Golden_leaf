class Product(object):
    def __init__(self,title, name, price, code,id=0):
        self.__id = id
        self.__title = title
        self.__name = name
        self.__price = price
        self.__code = code

    @property
    def id(self):
        """
        :return: id
        """
        return self.__id

    @id.setter
    def id(self, value):
        """
        Sets an attribute
        :param value: id
        :return: void
        """
        self.__id = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, string):
        self.__title = string

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, string):
        self.__name = string

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

    @property
    def code(self):
        return self.__code

    def __eq__(self, other):
        return self.__code == other.__code

    def __str__(self):
        return "Produto: {} {}, Código: {}, R$: {}" .format(self.__title,
                                                            self.__name,
                                                            self.__code,
                                                            self.__price,
                                                            )

