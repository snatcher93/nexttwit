nameTag = "Cho Young Ho"
messageBox = []

message = ""
while message != "QUIT":
    message = raw_input("Message to Write: ")
    if message != "QUIT":
        messageBox.append(message)
        
print nameTag, messageBox