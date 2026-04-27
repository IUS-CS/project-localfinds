import time
from werkzeug.security import generate_password_hash
from src.localfinds.models.posts import store_post
from src.localfinds.models.accounts import (
    store_account,
    get_account_by_username,
    update_account
)

def generate_data():
    accounts = "./data/accounts.db"
    posts = "./data/posts.db"

    store_account(accounts, "John", generate_password_hash("password"))
    update_account(accounts, get_account_by_username(accounts, "John").get("id"), "John", generate_password_hash("password"), bio="I enjoy pizza!")
    store_account(accounts, "Maddie", generate_password_hash("password"))
    update_account(accounts, get_account_by_username(accounts, "Maddie").get("id"), "Maddie", generate_password_hash("password"), bio="Asian cuizine is to die for!")
    store_account(accounts, "James", generate_password_hash("password"))
    update_account(accounts, get_account_by_username(accounts, "James").get("id"), "James", generate_password_hash("password"), bio="Avid gamer.")
    store_account(accounts, "Morgan", generate_password_hash("password"))
    update_account(accounts, get_account_by_username(accounts, "Morgan").get("id"), "Morgan", generate_password_hash("password"), bio="Player of all TCGs.")
    store_account(accounts, "Adam", generate_password_hash("password"))
    time.sleep(1)
    store_post(
        posts,
        "The New Albanian Brewing Company Pizzeria & Public House",
        "Great pizza, I reccomend the Upside Down. They have good drinks as well.",
        "John",
        "3312 Plaza Dr, New Albany, IN 47150",
        "pizza, beer",
    )
    time.sleep(1)
    store_post(
        posts,
        "Dragon King\'s Daughter",
        "Killer sushi, highly reccomend.",
        "Maddie",
        "129 W Market St, New Albany, IN 47150",
        "sushi",
    )
    time.sleep(1)
    store_post(
        posts,
        "Empire Comics & Games",
        "Great staff, wide selection of Magic: the Gathering cards. Plenty of board games and comics if you\'re into that kind of stuff.",
        "Morgan",
        "1636 Slate Run Rd, New Albany, IN 47150",
        "retro, comics, boardgames, magicthegathering, mtg, cards, tcg",
    )
    time.sleep(1)
    store_post(
        posts,
        "Asian Buffet",
        "What could be better than bottomless asian food?",
        "Maddie",
        "3813 Charlestown Rd, New Albany, IN 47150",
        "bottomless, asian",
    )
    time.sleep(1)
    store_post(
        posts,
        "Hollywood Movies and Games LLC",
        "Store is full of vintage videogames and pop culture memorabilia. Staff is friendly.",
        "James",
        "709B E Lewis and Clark Pkwy, Clarksville, IN 47129",
        "retro, videogames, collectibles, cards",
    )
    time.sleep(1)
    store_post(
        posts,
        "Arni\'s New Albany",
        "Decent service, decent pizza.",
        "John",
        "1208 State St, New Albany, IN 47150",
        "pizza",
    )
    time.sleep(1)
    store_post(
        posts,
        "Recbar 812",
        "Great place for a fun night of drinking and gaming.",
        "James",
        "336 Pearl St, New Albany, IN 47150",
        "retro, videogames, beer, arcade",
    )
    time.sleep(1)
    store_post(
        posts,
        "Rice Bowl Korean Restaurant",
        "Delicious large portions at an affordable price.",
        "Maddie",
        "3114 Grant Line Rd, New Albany, IN 47150",
        "korean",
    )
    time.sleep(1)
    store_post(
        posts,
        "Pearl Street Game & Coffee House",
        "Great place to drink coffe and shop for trading cards.",
        "Morgan",
        "405 Pearl St, Jeffersonville, IN 47130",
        "coffee, cafe, magicthegathering, mtg, cards, tcg",
    )
    time.sleep(1)
    store_post(
        posts,
        "Yellow Cactus",
        "Delicious mexican cuisine, large portions and fair prices.",
        "Adam",
        "3620 Paoli Pike, Floyds Knobs, IN 47119",
        "mexican, food",
    )
    time.sleep(1)
    store_post(
        posts,
        "The Slice",
        "Delicious pizza with a golf simulator available for rent.",
        "John",
        "1027 N Luther Rd, Georgetown, IN 47122",
        "pizza, golf",
    )