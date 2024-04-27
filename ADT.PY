from abc import ABC, abstractmethod

class Vehicle(ABC):
   
    
    @abstractmethod
    def start(self):
        
        pass
    
    @abstractmethod
    def stop(self):
       
        pass

class Car(Vehicle):
   
    
    def __init__(self, make, model):
        self._make = make
        self._model = model
        self._is_running = False
        
    def start(self):
       
        self._is_running = True
        print(f"{self._make} {self._model} has started.")

    def stop(self):
        
        if self._is_running:
            self._is_running = False
            print(f"{self._make} {self._model} has stopped.")
        else:
            print(f"{self._make} {self._model} is already stopped.")

# Usage Example:
if __name__ == "__main__":

    car = Car(make="Toyota", model="Camry")


    car.start()

  
    car.stop()

    # Try to stop the car again
    car.stop()
