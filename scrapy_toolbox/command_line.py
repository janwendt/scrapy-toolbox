import subprocess
import sys

def main():
    arg1 = sys.argv[1]
    if arg1:
        subprocess.check_output(["scrapy", "crawl", arg1, "-a process_errors=True"])

if __name__ == "__main__":
    main()
