import smtplib
from pynput.keyboard import Key, Listener
pressed_keys = ""
host_path = "C:/Windows/System32/drivers/etc/hosts"

with open("email_login","r") as file:
    content=file.read()
    print(content)



def sendemail():


    my_email = "221030109@juitsolan.in"
    password = "zuwmrqnvptaiiajd"
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()

    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs=content, msg="someone is accesing blocked website")
    connection.close()

def on_press(key):
    global pressed_keys
    try:

        pressed_keys += str(key.char)
    except AttributeError:

        pressed_keys += f' {str(key)} '

    check_blocked_words()

def write_1():
    pass

def on_release(key):
    if key == Key.esc:
        # If the pressed key is Esc, stop the listener
        return False

def check_blocked_words():
    global pressed_keys
    with open(host_path, "r") as host_file:
        content = host_file.read()
        for word in pressed_keys.split():

            if len(word) >= 4 and word in content:
                print(f"Blocked word detected: {word}")
                sendemail()

with Listener(on_press=on_press, on_release=on_release) as l:
    l.join()
    write_1()


