from multiprocessing import Process

#subclass Process 
class Worker(Process):
    def __init__(self, name):
        # Call the constructor of the parent class Process
        super(Worker, self).__init__()
        self.name = name

    def run(self):
        print(f'Worker {self.name} is running')

def main():
    workers = [Worker(str(i)) for i in range(5)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

if __name__ == "__main__":
    main()