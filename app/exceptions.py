class TariffNotFound(Exception):
    def __init__(self, message="Tariff not found"):
        self.message = message
        super().__init__(self.message)


class TariffConflict(Exception):
    def __init__(self, message="Tariff with this date and cargo type already exists"):
        self.message = message
        super().__init__(self.message)
