# Python DAO

An easy to use package to implement DAO pattern with your existing objects.

## Installation

    pip install git+https://github.com/mbml84/python-dao

### Use example :

    from python_dao.decorators import DecoratorFactory

    decorator = DecoratorFactory()

    class Person:

        def __init__(self, name: str, age: str):
            self.name = name
            self.age = age


    @decorator(Person):
    def get_persons_from_db() -> list[Person]:
        # Your code to fetch data from DB
        results = ...

        return results
