import asyncio



async def start_strongman(name, power):
    number_ball = 5
    print(f'Силач {name} начал соревнования')
    for ball in range(1, number_ball+1):
        await asyncio.sleep(5/power)
        print(f'Силач {name} поднял {ball} шар')
    print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Vasya', 5))
    task2 = asyncio.create_task(start_strongman('Georg', 4))
    task3 = asyncio.create_task(start_strongman('David', 3))
    await task1
    await task2
    await task3

asyncio.run(start_tournament())
