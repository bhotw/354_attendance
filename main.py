
import back_end.readerClass as re

newReader = re.ReaderClass()



while True:
    try:
        action = input("Sign in or Sign out or show: ")
        if action == "Sign in":
            newReader.attendance("in")
            newReader.greetins()
            newReader.showTable()
        elif action == "Sign out":
            newReader.attendance("out")
            newReader.bye()
        elif action == "show":
            howMany = input("How many: ")
            newReader.showTable(howMany)
        elif action == "write":
            newReader.write()
        else:
            print("Action not RECOGNIZED!!! Try again")
    except KeyboardInterrupt:
        newReader.destroy()
        break

