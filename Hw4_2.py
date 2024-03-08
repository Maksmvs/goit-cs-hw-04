import os
import multiprocessing
import time

class KeywordSearchProcess(multiprocessing.Process):
    def __init__(self, folder, keywords, result_queue):
        super().__init__()
        self.folder = folder
        self.keywords = keywords
        self.result_queue = result_queue

    def run(self):
        results = {}
        start_time = time.time_ns() // 1000

        for root, dirs, files in os.walk(self.folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r') as file:
                        text = file.read()
                        for keyword in self.keywords:
                            if keyword in text:
                                if keyword not in results:
                                    results[keyword] = set()  
                                results[keyword].add(file_path) 
                except Exception as e:
                    print(f"Помилка при обробці файлу {file_path}: {str(e)}")

        end_time = time.time_ns() // 1000
        self.result_queue.put((results, end_time - start_time))

def main():
    folder = r'D:\books'  
    keywords = ['сила']  
    result_queue = multiprocessing.Queue()

    processes = []
    for _ in range(2):
        process = KeywordSearchProcess(folder, keywords, result_queue)
        processes.append(process)
        process.start()

    total_results = {}
    total_time = 0

    for process in processes:
        process.join()
        results, time_taken = result_queue.get()
        total_time = max(total_time, time_taken)
        for keyword, files in results.items():
            if keyword not in total_results:
                total_results[keyword] = set() 
            total_results[keyword].update(files)  

        print(f"Процес {process.pid} виконався за {time_taken} мікросекунд")

    print("Результати пошуку:")
    for keyword, files in total_results.items():
        print(f"Ключове слово '{keyword}':")
        for file_path in files:
            print(f"- {file_path}")

    print(f"Загальний час виконання: {total_time} мікросекунд")

if __name__ == "__main__":
    main()
