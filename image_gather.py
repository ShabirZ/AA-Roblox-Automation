import time
import pyscreenshot as ImageGrab
import keyboard

# Function to take a screenshot and save it
def take_screenshot(count):
    filename = f"screenshot2_{count}.png"
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    print(f"Saved {filename}")

def main():
    x = int(input("Enter the interval (in seconds) between screenshots: "))
    print("Press 'q' to stop the program.")

    count = 1
    try:
        while True:
            take_screenshot(count)
            count += 1

            # Wait for x seconds, but break if 'q' is pressed
            for _ in range(x):
                if keyboard.is_pressed('q'):
                    print("Stopping...")
                    return
                time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated manually.")

if __name__ == "__main__":
    main()