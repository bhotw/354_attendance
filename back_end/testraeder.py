from back_end.readerClass import ReaderClass

reader = ReaderClass()

print("tap a card: ")
card_id, card_name = reader.read()
print("card id: ", card_id, " card name: ", card_name)