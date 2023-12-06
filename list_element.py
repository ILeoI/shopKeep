class ListElement:
    def __init__(self, displayText: str, selectable: bool = False, dataType: str = None, data: any = None):
        self.displayText = displayText
        self.selectable = selectable
        self.dataType = dataType
        self.data = data
