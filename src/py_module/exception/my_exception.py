class MyException(Exception):
    my_message = None

    def __init__(self, message, *args: object) -> None:
        super().__init__(*args)
        self.my_message = message