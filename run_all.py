import subprocess
from os import listdir
import os
import time
import threading

# A script to run all of the solutions.
# Will later be used be used for benchmarks
# and regression testing.

def main():
    proj_path = "../krax/src/sparv.csproj"

    subprocess.run(["dotnet", "build", proj_path,"--configuration", "Release", "-o", "./"], shell=True, capture_output=True)

    folders = [x for x in listdir("./") if x.startswith("day")]

    err_count = 0;
    for folder in folders:
        if not test_file(folder):
            err_count += 1
        else:
            print_ok(f"{folder} ok!")
    if err_count:
        print_err(f"{err_count} Error(s) occured in tests!")
    else:
        print(f"Err: {err_count}")
        print_ok("All tests Ok!")
    clean()

def timer(stop_timer, path):
    start_time = time.time()
    elapsed = 0
    try:
        while not stop_timer.is_set():
            time.sleep(0.1)  # Update every 0.1 seconds
            elapsed = time.time() - start_time
            print(f"{path}     {elapsed:.1f} seconds", end="\r")
    except KeyboardInterrupt:
        pass

def test_file(path: str):
    """
        runs the main.sparv file and compares it to the ans
        file.

        Args:
            path (str): Path to the folder where the main.sparv
            and ans file are located
        
        Returns:
            bool: Returns True if both of the cases are true.

    """
    file = open(path + "/ans", mode="r")
    answer = file.read().splitlines()

    
    stop_timer = threading.Event()
    try:
        timer_thread = threading.Thread(target=timer, args=(stop_timer, path,))
        timer_thread.start()

        output = subprocess.run(["sparv.exe", path + "/main.sparv"], shell=True, capture_output=True)
        actual = output.stdout.decode('utf-8').splitlines()

    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        stop_timer.set()
        timer_thread.join()

    error = answer[0] != actual[1] or answer[1] != actual[2]
    

    if error:
        print_err(f"\nError in test(s): '{path}'")
        print_err(f"Expected: {answer[0]}, actual: {actual[1]}")
        print_err(f"Expected: {answer[1]}, actual: {actual[2]}")

    return not error

def clean():
    files_to_delete = [
        "sparv",
        "Sparv.deps.json",
        "Sparv.dll",
        "Sparv.exe",
        "Sparv.pdb",
        "Sparv.runtimeconfig.json"
    ]
    for file in files_to_delete:
        if os.path.isfile(file):
            os.remove(file)



def print_ok(text):
    """ 
        Print green text.

        Args:
            text (str): The text to print.

        Returns:
            None
    """
    print(f"\033[92m{text}\033[0m")
def print_err(text):
    """ 
        Print red text.

        Args:
            text (str): The text to print.

        Returns:
            None
    """
    print(f"\033[91m{text}\033[0m")

if __name__ == "__main__": main()
