from typing import List

import list_element


# Element Stack
# 0 - First
# 1 - Second
# ...
# N - Last


class Page:
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title
        self.elements: List[list_element.ListElement] = []
        self.currentElementIndex = 0

    def addElement(self, element: list_element.ListElement):
        self.elements.append(element)

    def moveCursor(self, direction: int):
        # Move Up
        if direction == 0:
            # If not at top of page, move cursor
            if self.currentElementIndex == 0:
                self.currentElementIndex = len(self.elements) - 1
            else:
                self.currentElementIndex -= 1
        # Move Down
        if direction == 1:
            # If not at bottom of page, move cursor
            if self.currentElementIndex == len(self.elements) - 1:
                self.currentElementIndex = 0
            else:
                self.currentElementIndex += 1

    def getCurrentListElement(self):
        return self.elements[self.currentElementIndex]

    def getTextToDisplay(self):
        if len(self.elements) == 0:
            return (
                "None",
                "", 
                "",
            )
        if len(self.elements) >= 3:
            # If at first, show first three
            if self.currentElementIndex == 0:
                return (
                    self.elements[0].displayText + " <",
                    self.elements[1].displayText,
                    self.elements[2].displayText
                )

            # If at last, show last three
            elif self.currentElementIndex == len(self.elements) - 1:
                last = len(self.elements) - 1
                return (
                    self.elements[last - 2].displayText,
                    self.elements[last - 1].displayText,
                    self.elements[last].displayText + " <"
                )

            # Else, show one before, current, one after
            else:
                current = self.currentElementIndex
                return (
                    self.elements[current - 1].displayText,
                    self.elements[current].displayText + " <",
                    self.elements[current + 1].displayText
                )
        else:
            ret = []
            for i in range(0, len(self.elements)):
                if i == self.currentElementIndex:
                    ret.append(self.elements[i].displayText + " <")
                else:
                    ret.append(self.elements[i].displayText)
            return ret
