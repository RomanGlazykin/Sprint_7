class Order:
    def __init__(self, data):
        first_name = data.get('firstName')
        self.firstName = str(first_name) if first_name is not None else ""
        last_name = data.get('lastName')
        self.lastName = str(last_name) if last_name is not None else ""
        address = data.get('address')
        self.address = str(address) if address is not None else ""
        metroStation = data.get('metroStation')
        self.metroStation = str(metroStation) if metroStation is not None else ""
        phone = data.get('phone')
        self.phone = str(phone) if phone is not None else ""
        rentTime = data.get('rentTime')
        self.rentTime = int(rentTime) if rentTime is not None else 0
        deliveryDate = data.get('deliveryDate')
        self.deliveryDate = str(deliveryDate) if deliveryDate is not None else ""
        comment = data.get('comment')
        self.comment = str(comment) if comment is not None else "" # Обрабатываем comment
        self.color = data.get('color')
        self.id = data.get('id')

    def validate_fields(self):
        assert isinstance(self.firstName, str), "firstName is not a string"
        assert isinstance(self.lastName, str), "lastName is not a string"
        assert isinstance(self.address, str), "address is not a string"
        assert isinstance(self.metroStation, str), "metroStation is not a string"
        assert isinstance(self.phone, str), "phone is not a string"
        assert isinstance(self.rentTime, int), "rentTime is not an integer"
        assert isinstance(self.deliveryDate, str), "deliveryDate is not a string"
        assert isinstance(self.comment, str), "comment is not a string"
        if self.color is not None:
            assert isinstance(self.color, list), "color is not a list"
            for c in self.color:
                assert isinstance(c, str), "color element is not a string"
        assert isinstance(self.id, int), "id is not an integer"