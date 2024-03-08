import os
import threading
import time

class KeywordSearch(threading.Thread):
    def __init__(self, folder, keywords, result_dict):
        threading.Thread.__init__(self)
        self.folder = folder
        self.keywords = keywords
        self.result_dict = result_dict
        self.start_time = 0

    def run(self):
        self.start_time = time.time_ns() // 1000  
        for root, dirs, files in os.walk(self.folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r') as file:
                        text = file.read()
                        for keyword in self.keywords:
                            if keyword in text:
                                if keyword not in self.result_dict:
                                    self.result_dict[keyword] = set()  
                                self.result_dict[keyword].add(file_path)
                except Exception as e:
                    print(f"Помилка при обробці файлу {file_path}: {str(e)}")
        end_time = time.time_ns() // 1000 
        print(f"Thread {self.ident} finished in {end_time - self.start_time} microseconds")

def main():
    folder = r'D:\books'  
    keywords = ['життя']  

    result_dict = {}  

    
    threads = []
    for _ in range(2):  
        thread = KeywordSearch(folder, keywords, result_dict)
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()


    print("Результати пошуку:")
    for keyword, files in result_dict.items():
        print(f"Ключове слово '{keyword}':")
        for file_path in files:
            print(f"- {file_path}")

if __name__ == "__main__":
    main()
