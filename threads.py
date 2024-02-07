import subprocess
import threading

def run_script(script_path, *args):
    subprocess.run(['python', script_path] + list(args))

if __name__ == "__main__":
    script_path = 'a.py'  # Change this to the path of your script
    start = 2236202780  # Initial start value
    end = 2236202800  # Initial end value
    step = 20  # Step size
    dist = 45  # Distance value
    std = 12   # Standard value
    year = 2023  # Year value
    
    threads = []
    for _ in range(10):
        thread_args = ['--start=' + str(start), '--end=' + str(end), '--dist=' + str(dist), '--std=' + str(std), '--year=' + str(year)]
        thread = threading.Thread(target=run_script, args=(script_path,) + tuple(thread_args))
        threads.append(thread)
        thread.start()
        
        start = end + 1
        end = start + step
    
    for thread in threads:
        thread.join()
