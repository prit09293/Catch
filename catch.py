import subprocess
import asyncio
import re
import random
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError
from collections import deque

api_id = '29182205'
api_hash = '6104284ea05db7c126596a3a1a0a1271'
session = '"BQG9SP0AYgXYF_bkHUw_R1aErp1STdcv8FMgEmaL0PnaCgrLQ0dZS8lILZ9YWjc46PBVHPvaoRocj4fgNu72xptery5irCgK1PvtH1WivhbyecHHASLkCqHC3coQOxHO7C4A-nR82pdlShlLHQAmiyUEnF6IailXjeCm3M44ZBsJvHSEOVlrN6FNtWv8_UNB2qr_VDqUO_y-o4C7-VLsH_OCcEic7F_3HjvPdlivzDgntZGjTV5buv7TmurRRXKsijrbGaurZstiMymz6DKzz0_-0_PFqv8bhlwohORdRIHChn_Zz81XL1GBZv5BREJ-a7TpFR6yq-blf_Bvb4FoNgdc07U88wAAAAEv2RRbAA"'

clicked_4th_button = False

last_two_messages = deque(maxlen=2)

client = TelegramClient('your_session_file.session', api_id, api_hash)

legendary_poks = ["Rayquaza", "Kyogre", "Groudon", "Dialga", "Marshadow", "Reshiram", "Zekrom", "Yveltal", "Mewtwo", 
                  "Xerneas", "Zygarde", "Cosmog", "Cosmoem", "Necrozma", "Ho-oh", "Lugia", "Arceus", 
                  "Zeraora", "Pheromosa", "Mewtwo", "Victini", "Regigigas", "Deoxys", "Marshadow"]

regular_poks_repeat = ["Aerodactyl", "Rotom", "Minior", "Charizard", "Alakazam"]

regular_ball = ["Charmander", "Charmeleon", "Squirtle", "Wartortle", "Snorlax", "Abra", "Scyther"]

repeat_ball = regular_poks_repeat + legendary_poks
cooldown = random.randint(1, 2)
low_lvl = False

@client.on(events.NewMessage(from_users=5097722971))
async def dailyLimit(event):
    if "Daily hunt limit reached" in event.raw_text:
    	await client.disconnect()
    
    
@client.on(events.NewMessage(from_users=5097722971))
async def hunt_or_pass(event):
    if "✨ Shiny pokemon found!" in event.raw_text:  
        await event.client.send_message(-1004686399469, "@NARUTO_UZUMAKI07th shiny aaya jaldi dekho") 
        await client.disconnect()
    elif "A wild" in event.raw_text:
        global cooldown
        pok_name = event.raw_text.split("wild ")[1].split(" (")[0]
        print(pok_name)
        if pok_name in regular_ball or pok_name in repeat_ball:
            await asyncio.sleep(cooldown)
            await event.click(0, 0)
        else:
            await asyncio.sleep(cooldown)
            await client.send_message(5097722971, '/hunt')
            
            

@client.on(events.NewMessage(from_users=5097722971))
async def battlefirst(event):
    global low_lvl
    global cooldown
    if "Battle begins!" in event.raw_text:
        wild_pokemon_name_match = re.search(r"Wild (\w+) \[.*\]\nLv\. \d+  •  HP \d+/\d+", event.raw_text)
        
        if wild_pokemon_name_match:
            pok_name = wild_pokemon_name_match.group(1)
            
            wild_pokemon_hp_match = re.search(r"Wild .* \[.*\]\nLv\. \d+  •  HP (\d+)/(\d+)", event.raw_text)

            if wild_pokemon_hp_match:
                wild_max_hp = int(wild_pokemon_hp_match.group(2))
                if wild_max_hp <= 50:
                    low_lvl = True
                    print("low lvl set to true")
                    await asyncio.sleep(cooldown)
                    await event.click(text="Poke Balls")
                    print("cliked on btn poke balls")
                else:
                    await asyncio.sleep(2)
                    await event.click(0, 0)
                    
                    
 

import re
def calculate_health_percentage(max_hp, current_hp):
    if max_hp <= 0:
        raise ValueError("Total health must be greater than zero.")

    if current_hp < 0 or current_hp > max_hp:
        raise ValueError("Current health must be between 0 and the total health.")

    health_percentage = round((current_hp / max_hp) * 100)
    return health_percentage



@client.on(events.MessageEdited(from_users=5097722971))
async def battle(event):
    global low_lvl
    if "Wild" in event.raw_text:
        wild_pokemon_name_match = re.search(r"Wild (\w+) \[.*\]\nLv\. \d+  •  HP \d+/\d+", event.raw_text)

        if wild_pokemon_name_match:
            pok_name = wild_pokemon_name_match.group(1)

            wild_pokemon_hp_match = re.search(r"Wild .* \[.*\]\nLv\. \d+  •  HP (\d+)/(\d+)", event.raw_text)

            if wild_pokemon_hp_match:
                wild_max_hp = int(wild_pokemon_hp_match.group(2))
                wild_current_hp = int(wild_pokemon_hp_match.group(1))
                wild_health_percentage = calculate_health_percentage(wild_max_hp, wild_current_hp)
                if low_lvl == True:
                    await asyncio.sleep(cooldown)
                    await event.click(text="Poke Balls")
                    if pok_name in regular_ball:
                        await asyncio.sleep(1)
                        await event.click(text="Regular")
                    elif pok_name in repeat_ball:
                        await asyncio.sleep(1)
                        await event.click(text="Repeat")
                elif wild_health_percentage > 50:
                    await asyncio.sleep(1)
                    await event.click(0, 0)
                elif wild_health_percentage <= 50:
                    await asyncio.sleep(1)
                    await event.click(text="Poke Balls")
                    if pok_name in regular_ball:
                        await asyncio.sleep(1)
                        await event.click(text="Regular")
                    elif pok_name in repeat_ball:
                        await asyncio.sleep(1)
                        await event.click(text="Repeat")
                print(f"{pok_name} health percentage: {wild_health_percentage}%")
            else:
                print(f"Wild Pokemon {pok_name} HP not found in the battle description.")
        else:
            print("Wild Pokemon name not found in the battle description.")
            
            
            
            
@client.on(events.MessageEdited(from_users=5097722971))
async def skip(event):
    if any(substring in event.raw_text for substring in ["fled", "💵", "You caught"]):
        global cooldown
        global low_lvl
        low_lvl = False
        await asyncio.sleep(cooldown)
        await client.send_message(5097722971, '/hunt')        
    	
@client.on(events.NewMessage(from_users=5097722971))
async def skipTrainer(event):
    if "An expert trainer" in event.raw_text:
        global cooldown
        await asyncio.sleep(cooldown)
        await client.send_message(5097722971, '/hunt')        
 

@client.on(events.MessageEdited(from_users=5097722971))
async def pokeSwitch(event):
    if "Choose your next pokemon." in event.raw_text:
        buttons_to_click = ["Garchomp", "Sliggoo", "tapu bulu", "Rhyperior", "Hydreigon"]
        for button in buttons_to_click:
            try:
                await event.click(text=button)
            except:
                pass
                
                



   	
client.start()
client.run_until_disconnected()
