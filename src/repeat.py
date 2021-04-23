import threading

def printit():
  threading.Timer(1.0, printit).start()
  print("Hello, World!")

printit()

# continue with the rest of your code