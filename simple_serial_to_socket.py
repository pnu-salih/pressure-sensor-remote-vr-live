import serial, socket, time

SERIAL_PORT = "COM4"
BAUD = 9600
SERVER_IP = "192.168.50.60"
SERVER_PORT = 9000
SERIAL_TIMEOUT = 0.3

def main():
    while True:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD, timeout=SERIAL_TIMEOUT)
            print(f"Opened serial {SERIAL_PORT} @ {BAUD}")
            sock = socket.create_connection((SERVER_IP, SERVER_PORT), timeout=5)
            print(f"Connected to {SERVER_IP}:{SERVER_PORT}")
            try:
                while True:
                    line = ser.readline()
                    if not line:
                        continue
                    text = line.decode('utf-8', errors='ignore').strip()
                    if not text:
                        continue
                    sock.sendall((text + "\n").encode('utf-8'))
                    print(text)
            finally:
                sock.close()
                ser.close()
        except Exception as e:
            print("Error:", e, "- retrying in 3s")
            time.sleep(3)

if __name__ == "__main__":
    main()
