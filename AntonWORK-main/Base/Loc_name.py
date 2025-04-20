from aiogram import types
import asyncio
class Purse:
    def __init__(self,message:types.Message,latitude,longitude,str_username):
        locations = {}
        locations['latitude'] = latitude
        locations['longitude'] = longitude
        locations_for_write = [locations.get('latitude'),locations.get("longitude")]
        Loc_file_write=open('Locations.txt','a',encoding='utf-8')
        Loc_file_write.write(f'tg://user?id={str_username} - {locations_for_write[0]},{locations_for_write[1]}\n')
        Loc_file_write.close()
    async def answer_location(self,message:types.Message,locations_for_write):
        await message.answer_location(latitude=locations_for_write[0],longitude=locations_for_write[1])
        
        

