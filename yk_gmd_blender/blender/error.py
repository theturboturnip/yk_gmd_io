class GMDError(Exception):
    msg: str

    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(msg)