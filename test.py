import asyncio
async def showMsg():
    print("start...")
    await asyncio.sleep(2)
    print("end....")

async def funcMain():
    print("main step 1...")
    taskList=[asyncio.create_task(showMsg(),name="task1"),
              asyncio.create_task(showMsg(),name="task2")]
    print("main step 2...")
    done,padding=await asyncio.wait(taskList)
    print(done)

asyncio.run(funcMain())
# showMsgIns=showMsg()

# loop=asyncio.get_event_loop()
# loop.run_until_complete(showMsgIns)
# asyncio.run(showMsgIns)