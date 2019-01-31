import math
import random
import operator


class Basket:
    def __init__(self):
        self.items = []
        self.basket_total: int = 0

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __add__(self, other):
        """Add another baskets items."""
        for basket_item in other.items:
            self.items.append(basket_item)

    def __repr__(self):
        print(self.__sum__())

    def __call__(self):
        self.bill()

    def __sum__(self):
        total = sum(i.price for i in self.__iter__())
        self.basket_total = round(total, 2)
        return total

    def __sort__(self):
        self.items.sort(key=operator.attrgetter('name'))

    def print_items(self):
        for i in self.items:
            i()

    def recalculate_basket(self):
        self.__sum__()
        self.__sort__()

    def append(self, item):
        self.items.append(item)

    def bill(self):
        self.recalculate_basket()
        self.print_items()
        lines = []
        for i in self.__iter__():
            line = "{:24}{:>8}".format(i.name, i.price)

        s = ''.join((["-" for _ in range(0,33)]))
        lines.append(s)
        total_line = "{:24}{:>8}".format("Total", self.basket_total)
        lines.append(total_line)
        for l in lines:
            print(l)


class Item:
    def __init__(self, name: str, price: float):
        self.name: str = name
        self.price: float = price
        self.item = [self.name, self.price]

    def __call__(self):
        self.print_item()

    def __repr__(self):
        self.print_item()

    def print_item(self):
        print("{} {}".format(*self.item))

    def print_price(self):
        print(self.price)

if __name__ == "__main__":
    # Who's coming?
    def drinkers():
        num_drinkers = random.randint(2, 8)
        drinks_count = list([random.randint(1,5) for _ in range(0, num_drinkers)])
        return drinks_count


    # What's on tap?
    def rand_beer_price():
        return math.floor(random.uniform(3.40, 4.60) * 20) / 20


    woodforde_beers = (
        ("Wherry", rand_beer_price()),
        ("Norfolk Nog", rand_beer_price()),
        ("Nelson's Revenge", rand_beer_price()),
        ("Bure Gold", rand_beer_price()),
        ("Reedlighter", rand_beer_price()),
        ("Norada", rand_beer_price()),
        ("Headcracker", rand_beer_price()),
        ("Once Bittern", rand_beer_price()),
        ("Mardler's Mild", rand_beer_price()),
        ("Sundew", rand_beer_price()),
        ("Admiral's Reserve", rand_beer_price()),
        ("Tinsel Toes", rand_beer_price()),
        ("Simcoe Pale Ale", rand_beer_price()),
        ("West Coast Wherry", rand_beer_price()),
        ("Red Admiral", rand_beer_price()),
        ("Volt", rand_beer_price()),
        ("Tundra", rand_beer_price())
    )


    # Start drinking!
    def rand_beer():
        i = random.randint(0, len(woodforde_beers) - 1)
        return Item(*woodforde_beers[i])


    def append_to_tab(group, tab):
        for p in group:
            for b in range(0, p):
                beer = rand_beer()
                tab.append(beer)

    group_one = drinkers()
    group_one_tab = Basket()
    append_to_tab(group_one, group_one_tab)
    group_two = drinkers()
    group_two_tab = Basket()
    append_to_tab(group_two, group_two_tab)

    # First Tab
    group_one_tab()

    # Second Tab
    group_two_tab()

