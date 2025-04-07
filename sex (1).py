import subprocess
import asyncio
import re
import random
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError
from collections import deque

api_id = '29848170'
api_hash = 'e2b1cafae7b2492c625e19db5ec7f513'
session = '"1BVtsOH8Bu4FVmqgUEOPlLr_eCNE1LLZG6HYP-byyEwqkhlgqEBSnKD-E5R4mxJolZHfOx-X0Lpgjr3ApU_a0E-q2kaz7wUErqCWCVJxU4ZsMYasvF63OJEn553RXpFIi0SMnmJS1XHCQthYKksRnNba_Of3eOzUEyM95ftNoqTurHv_Ft-M0_tgmmM7x9ZYKf6EfFGEwjbsIlmf7rjcDv6gsOHt9vlQiRWiGc48tXAT02QHAuYMOy-e6nSOPB40p4l3BO6GufwiSnOkCtVdkIbQq9zukLHPLHq18iNlpUI6-Khx87E3McikCNEBVeEn_36KSurj6k9Pm67qCHfo0fAaOL1VXjzA="'

clicked_4th_button = False

last_two_messages = deque(maxlen=2)

client = TelegramClient('your_session_file.session', api_id, api_hash)

legendary_poks = ["Rayquaza", "Kyogre", "Groudon", "Dialga", "Kyurem", "Reshiram", "Zekrom", "Yveltal", 
                  "Xerneas", "Zygarde", "Cosmog", "Cosmoem", "Necrozma", "Ho-oh", "Lugia", "Arceus", 
                  "Zeraora", "Pheromosa", "Mewtwo", "Victini", "Regigigas", "Deoxys", "Marshadow"]

regular_poks_repeat = ["Aerodactyl", "Rotom", "Minior", "Charizard", "Alakazam"]

great_poks_ball = ["kadabra", "Charmeleon", "Charizard", "Wartortle", "Snorlax", "Abra", "Scyther", "Alakazam", "Gengar", "Haunter", "Gastly", "gyarados"]

ultra_balls = regular_poks_repeat + great_poks_ball
ultra_ball = legendary_poks
cooldown = random.randint(1, 2)
low_lvl = False

@client.on(events.NewMessage(from_users=572621020))
async def dailyLimit(event):
    if "Daily hunt limit reached" in event.raw_text:
    	await client.disconnect()
    
    
@client.on(events.NewMessage(from_users=572621020))
async def hunt_or_pass(event):
    if "✨ Shiny pokemon found!" in event.raw_text:  
        await event.client.send_message(-1002543449767, "@NARUTO_UZUMAKI07th shiny aaya jaldi dekho") 
        await client.disconnect()
    elif "A wild" in event.raw_text:
        global cooldown
        pok_name = event.raw_text.split("wild ")[1].split(" (")[0]
        print(pok_name)
        if pok_name in ultra_balls or pok_name in ultra_ball:
            await asyncio.sleep(cooldown)
            await event.click(0, 0)
        else:
            await asyncio.sleep(cooldown)
            await client.send_message(572621020, '/hunt')
            
            

@client.on(events.NewMessage(from_users=572621020))
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



@client.on(events.MessageEdited(from_users=572621020))
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
                    if pok_name in ultra_balls:
                        await asyncio.sleep(1)
                        await event.click(text="great")
                    elif pok_name in ultra_ball:
                        await asyncio.sleep(1)
                        await event.click(text="ultra")
                elif wild_health_percentage > 50:
                    await asyncio.sleep(1)
                    await event.click(0, 0)
                elif wild_health_percentage <= 50:
                    await asyncio.sleep(1)
                    await event.click(text="Poke Balls")
                    if pok_name in ultra_balls:
                        await asyncio.sleep(1)
                        await event.click(text="great")
                    elif pok_name in ultra_ball:
                        await asyncio.sleep(1)
                        await event.click(text="ultra")
                print(f"{pok_name} health percentage: {wild_health_percentage}%")
            else:
                print(f"Wild Pokemon {pok_name} HP not found in the battle description.")
        else:
            print("Wild Pokemon name not found in the battle description.")
            
            
            
            
@client.on(events.MessageEdited(from_users=572621020))
async def skip(event):
    if any(substring in event.raw_text for substring in ["fled", "💵", "You caught"]):
        global cooldown
        global low_lvl
        low_lvl = False
        await asyncio.sleep(cooldown)
        await client.send_message(572621020, '/hunt')        
    	
@client.on(events.NewMessage(from_users=572621020))
async def skipTrainer(event):
    if "An expert trainer" in event.raw_text:
        global cooldown
        await asyncio.sleep(cooldown)
        await client.send_message(572621020, '/hunt')        
 

@client.on(events.MessageEdited(from_users=572621020))
async def pokeSwitch(event):
    if "Choose your next pokemon." in event.raw_text:
        buttons_to_click = ["Aerodactyl", "Sandshrew", "Horsea", "Abra", "Bulbasaur"]
        for button in buttons_to_click:
            try:
                await event.click(text=button)
            except:
                pass
                
                



   	
client.start()
client.run_until_disconnected()
