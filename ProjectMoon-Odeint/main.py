from multiprocessing import Process, Queue, cpu_count
import simulation
import matplotlib.pyplot as plt
import numpy

process_list = []
angle_list = [] # narzędzie do testowania rysowania histogramu [numpy.random.normal(numpy.pi/4)*numpy.pi for _ in range(1000)]
q = Queue()


#Funkcja dodająca do kolejki wyniki Simulate()
def Proces(q, asteroid_number = 5, end = 9000  , frequency = 10000):
    q.put(simulation.Simulate(asteroid_number, end, frequency))

if __name__ == '__main__':
    
    for _ in range(cpu_count()):
        p = Process(target=Proces, args=(q,5,9000,10000))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    while not q.empty():
        angle_list += q.get()

#Rysowanie histogramu
    plt.hist(angle_list,[numpy.pi*i/30 for i in range(31)])
    plt.show()
