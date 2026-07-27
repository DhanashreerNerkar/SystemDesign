
#-----------------------------------Easy - Example 1------------------------------------------------
# Example 1: Easy Level (Basic Singleton)
class Singleton:
    _instance = None  # Class variable to hold the one instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# Usage
obj1 = Singleton()
obj2 = Singleton()

print(obj1 is obj2)  # True -> both point to the SAME object
print(id(obj1), id(obj2))  # Same memory address
#-------------------------------------Medium - Example 2----------------------------------------------
'''
Example 2: Medium Level (Thread-Safe Singleton with Lazy Initialization + Attributes)
Real applications run in multi-threaded environments (e.g., web servers). 
Without thread safety, two threads could both pass the if cls._instance is None check 
simultaneously and create two different instances — a race condition.

Example 2 solves two key problems:Thread-Safety: Ensures only one instance is created, 
even if 100 threads ask for it simultaneously.

Preventing Re-initialization: In Python, calling ClassName() always runs __init__. 
We need to make sure the object's initial values are set only once, not overwritten 
every time someone calls ConfigManager().

If two threads try to request the Singleton instance at the exact same millisecond, 
a standard Singleton can break. Both threads might check if the instance exists, 
see that it's None, and each create a separate instance. This creates a race condition and 
destroys the Singleton pattern.

##Object Creation (__new__) & Double-Checked Locking
First Check (if cls._instance is None):
Checks if the instance is already created. Once created, future calls skip the lock entirely, keeping the code fast.
with cls._lock::
If _instance is None, the thread acquires the lock. If another thread tries to enter at the same time, it is forced to wait.
Second Check (if cls._instance is None):
Once inside the lock, check again! Why? Because another thread might have been waiting at the lock door while the first thread was creating the instance. Without this second check, the waiting thread would enter and create a second instance.
cls._instance._initialized = False:
Prepares a flag so we know this new instance has not yet run its setup logic.

##Preventing Re-initialization (__init__):
Python automatically calls __init__ every single time you write ConfigManager(), 
even if __new__ returns an existing instance.
if self._initialized: return checks if the setup has already been completed. 
If it has, it exits immediately so existing settings are not wiped or overridden.

Goal,                       How Example 2 Shows It
Same Object Instance,       config1 is config2 returns True (both variables point to the exact same memory address).
Thread Safety,              Uses threading.Lock() and Double-Checked Locking to avoid race conditions.
State Protection,           "Passing a new argument like ConfigManager(""different_config.yaml"") is ignored because _initialized prevents overwriting the original settings."
'''

import threading

class ConfigManager:
    _instance = None
    _lock = threading.Lock()  # Ensures only one thread creates the instance. 
                              # Creates a synchronization lock shared across all instances of the class. 
                              # Only one thread can hold this lock at a time.

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:  # Acquire lock before checking again ("double-checked locking")
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path="config.yaml"):
        if self._initialized:
            return  # Prevent re-initializing on subsequent calls
        self.config_path = config_path
        self.settings = {"debug": False, "env": "production"}  # Simulated loaded config
        self._initialized = True

    def get_setting(self, key):
        return self.settings.get(key)


# Usage
config1 = ConfigManager("app_config.yaml")
config2 = ConfigManager("different_config.yaml")  # This path is ignored!

print(config1 is config2)  # True
print(config1.config_path)  # "app_config.yaml" (only set once)
print(config2.get_setting("env"))  # "production"


#--------------------------------------Hard - Example 3---------------------------------------------
'''
In Example 2 (the Medium level), we built a thread-safe Singleton by adding custom __new__, __lock__, and _initialized logic inside a specific class (like ConfigManager).
However, in professional production codebases, you might have 10 different classes that need to be Singletons (e.g., DatabaseConnectionPool, Logger, CacheManager, ApiClient).
If you used Example 2's approach, you would have to copy and paste 20+ lines of locking and initialization boilerplate code into every single class. That violates the DRY (Don't Repeat Yourself) principle and makes code hard to maintain.

Metaclass in Python?
A standard class is a blueprint for creating objects (instances).
A metaclass is a blueprint for creating classes.
In Python, when you call MyClass(), Python executes the __call__ method of MyClass's metaclass!

By overriding __call__ on a metaclass (SingletonMeta), we intercept the moment someone tries to instantiate any class that uses this metaclass.

1. _instances = {}
A dictionary mapping a class (e.g., DatabaseConnectionPool) to its single instance.
Because _instances lives on SingletonMeta, one single dictionary manages all singletons in the entire application!

2. _lock = threading.Lock()
Ensures thread-safety across all threads attempting to create singletons concurrently.

3. def __call__(cls, *args, **kwargs):
cls represents the class being instantiated (for example, DatabaseConnectionPool).
When someone writes db = DatabaseConnectionPool(), Python runs SingletonMeta.__call__(DatabaseConnectionPool).

4. Double-Checked Locking inside __call__
Outer Check (if cls not in cls._instances): Checks if an instance for this specific class already exists in the _instances dictionary. If it does, skip locking entirely and return it immediately (high performance).
Locking (with cls._lock:): If no instance exists, acquire the thread lock so only one thread can proceed.
Inner Check (if cls not in cls._instances): Re-checks to ensure another thread didn't create the instance while this thread was waiting for the lock.
instance = super().__call__(*args, **kwargs): Executes the target class's standard __init__ constructor.
cls._instances[cls] = instance: Stores the instance in the dictionary so all future calls receive the exact same object.

Notice how clean DatabaseConnectionPool and Logger are! They don't contain any thread-locking logic, __new__ overrides, or _initialized flags. All Singleton magic is cleanly isolated inside metaclass=SingletonMeta.
'''

import threading

class SingletonMeta(type):
    """
    A thread-safe metaclass that turns ANY class using it into a Singleton.
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # Double-checked locking pattern
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnectionPool(metaclass=SingletonMeta):
    def __init__(self, host="localhost", max_connections=10):
        print(f"Initializing connection pool to {host} with {max_connections} connections...")
        self.host = host
        self.max_connections = max_connections
        self.active_connections = 0
        self._pool_lock = threading.Lock()

    def acquire_connection(self):
        with self._pool_lock:
            if self.active_connections >= self.max_connections:
                raise RuntimeError("Connection pool exhausted!")
            self.active_connections += 1
            return f"Connection-{self.active_connections}"

    def release_connection(self):
        with self._pool_lock:
            if self.active_connections > 0:
                self.active_connections -= 1


class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.logs = []

    def log(self, message):
        self.logs.append(message)
        print(f"[LOG]: {message}")


# Usage
db1 = DatabaseConnectionPool(host="prod-db-server", max_connections=5)
db2 = DatabaseConnectionPool(host="ignored-different-host")  # Ignored, same instance returned

print(db1 is db2)  # True
print(db1.host)  # "prod-db-server"

conn = db1.acquire_connection()
print(conn)  # Connection-1

logger1 = Logger()
logger2 = Logger()
print(logger1 is logger2)  # True — a completely separate Singleton class, independent of DatabaseConnectionPool


'''
Level	    Technique	                Thread-Safe?	Reusable across classes?
-----------------------------------------------------------------------------------
Easy	    __new__ override	        ❌ No	        ❌ No
Medium	    __new__ + threading.Lock	✅ Yes	        ❌ No
Hard	    Metaclass (SingletonMeta)	✅ Yes	        ✅ Yes
'''