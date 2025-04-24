import sys
import os
import time
from tqdm import tqdm
from scapy.all import *

def hexdump(pkt, length=16):
    src = bytes(pkt)
    HEX_FILTER = ''.join(
        [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]
    )

    results = []
    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length * 3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    return results

def packet_handler(pkt):
    if pkt.haslayer(Raw):
        print_hexdump(pkt.load)

def print_hexdump(src, length=16):
    with tqdm(total=len(src)) as pbar:
        for line in hexdump(src, length):
            print(line)
            pbar.update(1)
            time.sleep(0.1)

# ホストOSから送られたテキストファイルのパスをコマンドライン引数から取得
file_path = sys.argv[1]

try:
    # テキストファイルが見つかるまで待機
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time >= 30:
            print("30 minutes elapsed. Exiting program.")
            break
        time.sleep(1)
    else:
        # テキストファイルを読み取りモードで開く
        with open(file_path, "r") as file:
            content = file.read()
            packet_handler(content)
except KeyboardInterrupt:
    print("Ctrl+C detected. Exiting program.")
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print("An error occurred:", e)
