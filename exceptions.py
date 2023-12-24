class Data_Structure_Error(Exception):
    def __init__(self, message = "Parsed dividend data is incomplete and/or have missing data.") -> None:
        self.message = message

        super().__init__(self.message)


class Dividend_Data_Error(Exception):
    def __init__(self, message = "There are no parsed data from Reference Website.") -> None:
        self.message = message

        super().__init__(self.message)
