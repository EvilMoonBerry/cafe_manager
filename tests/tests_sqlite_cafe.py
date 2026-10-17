from dotenv import load_dotenv
from db.sqlite_cafe import cafe_menu
from db.sqlite_cafe import cafe_staff

load_dotenv()


# Tests for the functionalities for manipulating menu.db
print(cafe_menu.list_all())

print(cafe_menu.get(3))

new_item = cafe_menu.add(
    {"name": "Green tea", "category": "Pastry", "price": 3.30, "in_stock": 1}
)

print("Addedd new item to menu.db:", new_item, cafe_menu.get(new_item))

cafe_menu.update(
    new_item, {"name": "Green tea", "category": "Pastry", "price": 3.30, "in_stock": 0}
)

print("Updated menu.db:", cafe_menu.get(new_item))

cafe_menu.delete(new_item)
print("Deleted item from menu.db: ", cafe_menu.get(new_item))

# Tests for the functionalities for manipulating staff.db

print(cafe_staff.list_all())

print(cafe_staff.get(3))

new_person = cafe_staff.add(
    {"name": "Ella", "role": "Barista", "hourly_wage": 16.00, "starting_date": "2026-8-8"}
)

print("Addedd new person to staff.db:", new_person, cafe_staff.get(new_person))

cafe_staff.update(
    new_person, {"name": "Ella", "role": "Barista", "hourly_wage": 17.50, "starting_date": "2026-8-8"}
)

print("Updated person from staff.db:", cafe_staff.get(new_person))

cafe_staff.delete(new_person)
print("Deleted person from staff.db: ", cafe_staff.get(new_person))