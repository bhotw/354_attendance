from readerClass import ReaderClass

reader = ReaderClass()

print("tap a card: ")
card_id, card_name = reader.read()
print("card id: ", card_id, " card name: ", card_name)
print("Tap a card for only card id: ")
card_id = reader.read_id()
print("only card id: ", card_id)
