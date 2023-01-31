import sysv_ipc
 
key = 128
 
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
 
value = 1
while value:
    try:
        value = int(input())
    except:
        print("Input error, try again!")
    message = str(value).encode()
    mq.send(message)
 
mq.remove()