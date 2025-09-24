import serial
import socket
import time
import threading
import queue
import sys

# --- CONFIG ---
SERIAL_PORT = "COM3"
BAUD = 115200
SERVER_IP = "192.168.50.60" # Unity PC
SERVER_PORT = 9000
QUEUE_MAX = 500

q = queue.Queue(maxsize=QUEUE_MAX)

def serial_reader():
    while True:
        try:
            with serial.Serial(SERIAL_PORT, BAUD, timeout=1) as ser:
                print(f"Opened serial {SERIAL_PORT} @ {BAUD}")
                while True:
                    line = ser.readline().decode("utf-8", errors="ignore").strip()
                    if line:
                        try:
                            q.put_nowait(line)
                        except queue.Full:
                            try:
                                q.get_nowait()
                                q.put_nowait(line)
                            except:
                                pass
        except Exception as e:
            print("Serial error:", e)
            time.sleep(2)

def socket_sender():
    while True:
        try:
            print(f"Connecting to {SERVER_IP}:{SERVER_PORT} ...")
            with socket.create_connection((SERVER_IP, SERVER_PORT), timeout=5) as sock:
                print("Connected to server.")
                while True:
                    value = q.get()  # blocks until item available
                    msg = (value + "\n").encode("utf-8")
                    try:
                        sock.sendall(msg)
                    except Exception as e:
                        try:
                            q.put_nowait(value)
                        except queue.Full:
                            pass
                        raise
        except Exception as e:
            print("Socket error / reconnecting in 5s:", e)
            time.sleep(5)

if __name__ == "__main__":
    t1 = threading.Thread(target=serial_reader, daemon=True)
    t2 = threading.Thread(target=socket_sender, daemon=True)
    t1.start()
    t2.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting.")
        sys.exit(0)
