class Data_Structure_Error(Exception):
    def __init__(self, message = "Parsed dividend data is incomplete and/or have missing data.") -> None:
        self.message = message

        super().__init__(self.message)


class Dividend_Data_Error(Exception):
    def __init__(self, message = "There are no parsed data from Reference Website.") -> None:
        self.message = message

        super().__init__(self.message)

class Mode_Error(Exception):
    def __init__(self, message = "The MODE you pass is invalid. Either pass |ticker|,|name|, or |all| ") -> None:
        self.message = message

        super().__init__(self.message)

class Edit_Mode_Error(Exception):
    def __init__(self, message = "The EDIT MODE you pass is invalid. Either pass |overwrite|, |append|, or |update| ") -> None:
        self.message = message

        super().__init__(self.message)


class Company_Info_Error(Exception):
    def __init__(self, company_name, message = "Company Info you passed seems to be absent from the PSE Listed Companies. Check your input and try again.") -> None:
        self.message = f"Problem with INPUT -'{company_name}':" + message

        super().__init__(self.message)
