
import signal
import subprocess


def main():
    processes = []
    process_app = None
    process_market = None
    process_bomb_1 = None
    process_bomb_2 = None
    process_color_1 = None
    process_color_2 = None
    process_hack = None
    process_found = None
    try:
        # process_app = subprocess.Popen(['python', 'app.py'])
        process_market = subprocess.Popen(['python', 'marketGather.py'])
        process_bomb_1 = subprocess.Popen(['python', 'bombExplode1.py'])
        process_bomb_2 = subprocess.Popen(['python', 'bombExplode2.py'])
        process_color_1 = subprocess.Popen(['python', 'coror_manager1.py'])
        process_color_2 = subprocess.Popen(['python', 'coror_manager2.py'])
        process_hack = subprocess.Popen(['python', 'hackAdd.py'])
        process_found = subprocess.Popen(['python', 'autofund.py'])
        processes = [process_app, process_market, process_bomb_1, process_bomb_2, process_color_1, process_color_2,
                     process_hack, process_found]

        process_bomb_1.wait()
    except KeyboardInterrupt:
        for proc in processes:
            if proc:
                proc.send_signal(signal.CTRL_C_EVENT)


if __name__ == "__main__":
    main()
