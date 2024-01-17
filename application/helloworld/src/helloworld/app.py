import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import httpx


class HelloWorld(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN,background_color = "lightGray"))
        add_product_box = toga.Box(style=Pack(direction=ROW,background_color = "lightPink"))

        name_label = toga.Label(
            "requesting to JSONPlaceholder:",
            style=Pack(padding=(5))
        )

        add_product_box_label = toga.Label(
            "manage your products",
            style=Pack(padding=(5))
        )



        self.name_input = toga.TextInput(style=Pack(flex=2, padding=5,font_size = 8),placeholder  = "a number between 0 & 99")
        self.section_input = toga.TextInput(style=Pack(flex=1, padding=5,font_size = 8),placeholder  = "title or body")
        self.product_name_input = toga.TextInput(style=Pack( padding=5,font_size = 8),placeholder  = "enter your product name")
        self.product_quantity_input = toga.TextInput(style=Pack( padding=5,font_size = 8),placeholder  = "enter the quantity of your product")
        self.product_buy_price_input = toga.TextInput(style=Pack( padding=5,font_size = 8),placeholder  = "enter the buy price")


        name_box = toga.Box(style=Pack(direction=COLUMN, padding=5,background_color = "lightBlue"))
        name_box.add(name_label)
        add_product_box.add(add_product_box_label)
        name_box.add(self.name_input)
        name_box.add(self.section_input)
        


        button = toga.Button(
            "httpx request to post",
            on_press=self.say_hello,
            style=Pack(padding=5)
        )

        add_product_bottun = toga.Button(
            "add a product",
            on_press=self.add_product,
            style=Pack(padding=5,flex=1)
        )

        #main_box.add(name_box)
        #main_box.add(button)
        add_product_box.add(self.product_name_input)
        add_product_box.add(self.product_quantity_input,self.product_buy_price_input)
        add_product_box.add(add_product_bottun)
        
        

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.content.add(add_product_box)
        self.main_window.show()

    async def say_hello(self, widget):
        async with httpx.AsyncClient() as client:
            response = await client.get("https://jsonplaceholder.typicode.com/posts")

        payload = response.json()
        
        try :
            self.main_window.info_dialog("hello",
                payload[int(self.name_input.value)][self.section_input.value],
                )
        except (ValueError ,IndexError):
            self.main_window.info_dialog("hey","please enter a number in range 0 & 99")
        except KeyError:
            self.main_window.info_dialog("hey","please enter one of these: title or body in 2nd input field")
    
    index_of_products = 0
    list_of_names = []
    list_of_indexes = []
    list_of_in_stocks = []
    list_of_total_product_sells = []
    total_sold = 0
    total_buy = 0

    def add_product(self,widget):
        my_index = self.index_of_products
        sold_product_box = toga.Box(style=Pack(direction=COLUMN, padding=5,background_color = "blue"))
        sold_box = toga.Box(style=Pack(direction=COLUMN, padding=5,background_color = "blue"))
        product_box = toga.Box(style=Pack(direction=ROW, padding=5,background_color = "blue"))
        total_product_sell_box = toga.Box(style=Pack(direction=ROW, padding=5,background_color = "blue"))

        if my_index == 0:
            all_products_box = toga.Box(style=Pack(direction=ROW, padding=1))

        self.list_of_indexes.append(my_index)
        self.index_of_products += 1

        quantity = int(self.product_quantity_input.value)
        in_stock = quantity
        self.list_of_in_stocks.append(in_stock)

        price = int(self.product_buy_price_input.value)
        total_product_buy_price = quantity* price
        self.total_buy += total_product_buy_price
        button = toga.Button(
            f"you bought {quantity} of {self.product_name_input.value} for {price} for each one",
            style=Pack(direction=ROW,padding=5,flex=1)
        )
        self.list_of_names.append(self.product_name_input.value)

        in_stock_button = toga.Button(
            f"you have {in_stock} of {self.list_of_names[my_index]} in stock.",
            style=Pack(direction=ROW,padding=5,flex=1)
        )



        total_product_sell = 0
        self.list_of_total_product_sells.append(total_product_sell)

        total_product_sell_button = toga.Button(
            f"You sold {self.list_of_total_product_sells[my_index]} of {self.list_of_names[my_index]}",
            style=Pack(direction=ROW,padding=5,flex=1)
        )

        total_product_buy_button = toga.Button(
            f"total buy price is : {total_product_buy_price}",
            style=Pack(direction=ROW,padding=5,flex=1)
        )

        sell_price_input = toga.TextInput(style=Pack( padding=5,font_size = 8),placeholder  = "enter the sell price")
        sell_quantity_input = toga.TextInput(style=Pack( padding=5,font_size = 8),placeholder  = "enter the sell quantity")

        if my_index == 0:

            self.total_sold_button = toga.Button(
                f"total sold : {self.total_sold}",
                style=Pack(padding=5)
            )

            self.total_buy_button = toga.Button(
                f"total buy : {self.total_buy}",
                style=Pack(padding=5)
            )

            self.earn_button = toga.Button(
                f"money earn : {self.total_sold - self.total_buy}",
                style=Pack(padding=5)
            )
        else :
            self.total_buy_button.text = f"total buy : {self.total_buy}"
            self.earn_button.text = f"money earn : {self.total_sold - self.total_buy}"




        def sell(widget):

            if sell_quantity_input.value and sell_price_input.value:
                sell_quantity = int(sell_quantity_input.value)
                sell_price = int(sell_price_input.value)
            else:
                self.main_window.info_dialog("unknown sell","you need to enter sell quantity & price.")

            if sell_quantity <= self.list_of_in_stocks[my_index]:
                sold_button = toga.Button(
                f"you sold {sell_quantity} of {self.list_of_names[my_index]} for {sell_price} for each one",
                style=Pack(padding=5)
                )
                sold_box.add(sold_button)
                self.list_of_in_stocks[my_index] -= sell_quantity
                self.total_sold += sell_quantity * sell_price
                self.total_sold_button.text = f"total sold : {self.total_sold}"
                self.earn_button.text = f"money earn : {self.total_sold - self.total_buy}"
                self.list_of_total_product_sells[my_index] += sell_quantity * sell_price
                total_product_sell_button.text = f"You sold {self.list_of_total_product_sells[my_index]} of {self.list_of_names[my_index]}"
                in_stock_button.text = f"you have {self.list_of_in_stocks[my_index]} of {self.list_of_names[my_index]} in stock."

            else:
                self.main_window.info_dialog("lack of product","you can't sell more than you have in stock.")



        sell_button = toga.Button(
            "sell",
            on_press=sell,
            style=Pack(padding=5)
        )

        


        if my_index == 0:
            all_products_box.add(self.total_sold_button,self.total_buy_button,self.earn_button)
            product_box.add(button,total_product_buy_button,sell_button,sell_quantity_input,sell_price_input)
            total_product_sell_box.add(total_product_sell_button,in_stock_button)
            sold_product_box.add(product_box,sold_box,total_product_sell_box)
            all_products_box.add(sold_product_box)
            self.main_window.content.add(all_products_box)
        product_box.add(button,total_product_buy_button,sell_button,sell_quantity_input,sell_price_input)
        total_product_sell_box.add(total_product_sell_button,in_stock_button)
        sold_product_box.add(product_box,sold_box,total_product_sell_box)
        self.main_window.content.add(sold_product_box)
    





def main():
    return HelloWorld()        