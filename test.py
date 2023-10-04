from subprocess import PIPE, Popen, check_output

# import subprocess
# import asyncio
# from asyncio.subprocess import Process

# async def command():
#     print('started')
#     results = await asyncio.create_subprocess_exec('/home/wethinkcode_/.local/bin/wtc-lms', 'reviews') 
#     print('ended')
#     stdout, stderr = await results.communicate()
#     returncode = results.returncode
#     return returncode, stdout, stderr

# asyncio.run(command())

# txt = "just a string [target] dummy"


# def extract_status(text):
#     start, end = text.index("["), text.find("]")+1
#     return text[start:end]


# print(extract_status(txt))


print("started")

results = Popen(["wtc-lms", "reviews"], stdout=PIPE, universal_newlines=True)
l = results.communicate()
print(l[0])
print("Ended")
results.stdout.close()
