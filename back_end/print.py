
from back_end.dataMan import DataMan

class Print:

    def showTable(self, howMany = "all"):
        if howMany == "one":
            DataMan.print(self)
        elif howMany == "all":
            DataMan.printAll(self)
        else:
            print("Try: one or all")