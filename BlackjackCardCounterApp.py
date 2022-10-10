"""
Maintains running count of cards dealt in a game of blackjack.
"""
import toga
from toga.style.pack import COLUMN, LEFT, RIGHT, ROW, Pack


def build(app):
    decksInShoe_box = toga.Box()
    count_box = toga.Box()
    remaining_box = toga.Box()
    trueCount_box = toga.Box()
    box = toga.Box()

    decksInShoe_input = toga.TextInput()
    decksInShoe_input.value = 1
    count = toga.TextInput(readonly=True)
    count.value = 0
    remaining = toga.TextInput(readonly=True)
    remaining.value = 52 * int(decksInShoe_input.value)
    trueCount = toga.TextInput(readonly=True)
    trueCount.value = 0
    
    decksInShoe_label = toga.Label('decks in shoe')
    count_label = toga.Label('count', style=Pack(text_align=LEFT))
    remaining_label = toga.Label('remaining cards', style=Pack(text_align=LEFT))
    trueCount_label = toga.Label('true count', style=Pack(text_align=LEFT))

    def high(widget):
        count.value = int(count.value) - 1
        remaining.value = int(remaining.value) - 1
        trueCount.value = int(count.value) * 52 / int(remaining.value)
            
    def low(widget):
        count.value = int(count.value) + 1
        remaining.value = int(remaining.value) - 1
        trueCount.value = int(count.value) * 52 / int(remaining.value)
            
    def mid(widget):
        remaining.value = int(remaining.value) - 1
        trueCount.value = int(count.value) * 52 / int(remaining.value)
        
    def shuffle(widget):
        count.value = 0
        try:
            remaining.value = 52 * max(int(decksInShoe_input.value), 0)
        except:
            remaining.value = 0
        trueCount.value = 0
        

    lowButton = toga.Button('Low', on_press=low)
    midButton = toga.Button('Mid', on_press=mid)
    highButton = toga.Button('High', on_press=high)
    shuffleButton = toga.Button('Shuffle', on_press=shuffle)
    
    decksInShoe_box.add(decksInShoe_input)
    decksInShoe_box.add(decksInShoe_label)
    count_box.add(count)
    count_box.add(count_label)
    remaining_box.add(remaining)
    remaining_box.add(remaining_label)
    trueCount_box.add(trueCount)
    trueCount_box.add(trueCount_label)

    box.add(decksInShoe_box)
    box.add(count_box)
    box.add(remaining_box)
    box.add(trueCount_box)
    box.add(highButton)
    box.add(midButton)
    box.add(lowButton)
    box.add(shuffleButton)

    box.style.update(direction=COLUMN, padding_top=10)
    decksInShoe_box.style.update(direction=ROW, padding=5)
    count_box.style.update(direction=ROW, padding=5)
    remaining_box.style.update(direction=ROW, padding=5)
    trueCount_box.style.update(direction=ROW, padding=5)

    decksInShoe_input.style.update(flex=0, padding_left=160)
    count.style.update(flex=0, padding_left=160)
    remaining.style.update(flex=0, padding_left=160)
    trueCount.style.update(flex=0, padding_left=160)
    decksInShoe_label.style.update(width=100, padding_left=10)
    count_label.style.update(width=100, padding_left=10)
    remaining_label.style.update(width=100, padding_left=10)
    trueCount_label.style.update(width=100, padding_left=10)

    highButton.style.update(padding_top=50, flex=1)
    midButton.style.update(padding_top=15, flex=1)
    lowButton.style.update(padding_top=15, flex=1)
    shuffleButton.style.update(padding_top=50, flex=1)

    return box


def main():
    return toga.App('Blackjack Card Counter', 'com.justdoitdt', startup=build)


if __name__ == '__main__':
    main().main_loop()
