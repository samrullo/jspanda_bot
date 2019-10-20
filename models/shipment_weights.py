from models.model import Model


class ShipmentWeights(Model):
    def __init__(self):
        super().__init__()
        self.table = "shipment_weights"

    def create(self):
        statement=""
