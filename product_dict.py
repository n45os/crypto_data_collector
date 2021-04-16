from coingecko import CGapi


import json


cg = CGapi()


class Product_dict:

    def __init__(self):
        self.prod_dict = self.retrieve_prod_dict_from_file()

    def retrieve_prod_dict_from_file(self):
        from os import path, getcwd
        cur = getcwd()
        with open(cur + "/info/product_dict.dat", "r") as f:
            return json.load(f)

    def ask_for_verification(self):
        while True:
            print("look at the prodocts that I will collect data from:\n")
            i = 1
            for p in self.prod_dict["products"]:
                print(f"{i}. {p}")
                i+= 1
            in1 = input("\n do you want to add more?(y/n)")
            if in1.lower() == "y":
                self.add_product()
                continue
            print("\nso lets start!")
            break

    def add_product(self):
        print("\n\n---PRODUCT ADDITION\n")
        while True:
            in1 = input("type the product that you wanna add")
            if in1 in self.prod_dict['products']:
                print("product already in list")
                continue
            else:
                ver , prod_dict = cg.find_new_product_in_coinlist(prod= in1)
                if ver:
                    self.prod_dict["products"].append(in1)
                    self.update_dict_file()
                    print('product added!')
                    break
                else:
                    print("try again")
                    continue

    def update_dict_file(self):
        from os import path, getcwd
        cur = getcwd()
        with open(cur + "/info/product_dict.dat", "w") as f:
            json.dump(self.prod_dict, f, indent=4)




