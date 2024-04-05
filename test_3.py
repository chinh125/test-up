import random
import time
def main():
    random_number = random.randint(1, 2)
    question = "Anh ta có thích bạn không? "
    print(question)
    time.sleep(2)
    if random_number == 1:
        print("Anh ta thích bạn và sẽ nhắn tin cho bạn.")
    else:
        print("Anh ta không thích bạn và bạn sẽ để ảnh ghost.")

if __name__ == "__main__":
    main()
