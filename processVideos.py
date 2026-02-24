#here videos will be converted into audios
import os
import subprocess

files=os.listdir("videos")
for file in files:
    file_number=file.split(" [")[0].split(" #")[1]
    file_name=file.split(" ｜ ")[0]
    print(file_number,file_name)
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{file_number}_{file_name}.mp3"])
