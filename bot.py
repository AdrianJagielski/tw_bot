import socket
d = {}
with open("config.txt") as f:
    for line in f:
       (key, val) = line.split()
       d[key] = val

HOST = d['HOST']
PORT = int(d['PORT'])
NICK = d['NICK']
PASS = d['PASS']

with open("banned_words.txt") as f:
    banned_words = [word for word in f]
banned_words = [_.replace('\n','') for _ in banned_words]

with open("commands.txt") as f:
    commands = [word for word in f]
commands = [_.replace('\n','') for _ in commands]


def send_message(message):
    s.send(bytes("PRIVMSG #" + NICK + " :" + message + "\r\n", "UTF-8"))


def del_message():
    s.send(bytes("PRIVMSG #" + NICK + " :" + ".timeout " + username + " 1" + "\r\n", "UTF-8"))

s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #kigiro" +" \r\n", "UTF-8"))



while True:
    r_buf = s.recv(1024).decode()
    temp = r_buf.split("\n")
    temp.pop()
    for line in temp:
        # Checks whether the message is PING because its a method of Twitch to check if you're afk
        if (line[0] == "PING"):
            s.send(bytes("PONG %s\r\n" % line[1],"UTF-8"))
        else:
            # Splits the given string so we can work with it better
            parts = line.split(":")
            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:
                    # Sets the message variable to the actual message sent
                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""
            usernamesplit = parts[1].split("!")
            username = usernamesplit[0]

            if message == "Hey":
                send_message("Welcome to my stream, " + username)
            if any(x in message for x in banned_words):
                del_message()
            if message == "!help":
                send_message("Commands: "+ commands)






