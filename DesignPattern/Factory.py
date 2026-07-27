#-------------------------------------------------
# #Example 1: Easy Level (Basic Factory Method)
#---------------------------------------------
from abc import ABC, abstractmethod
from email.mime import message

# Product interface
class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass


# Concrete Products
class Circle(Shape):
    def draw(self):
        return "Drawing a Circle"


class Square(Shape):
    def draw(self):
        return "Drawing a Square"


# Factory Method (simple function-based factory)
def shape_factory(shape_type):
    if shape_type == "circle":
        return Circle()
    elif shape_type == "square":
        return Square()
    else:
        raise ValueError(f"Unknown shape type: {shape_type}")


# Usage
shape1 = shape_factory("circle")
shape2 = shape_factory("square")

print(shape1.draw())  # Drawing a Circle
print(shape2.draw())  # Drawing a Square

#---------------------------------------------------------------------
#Example 2: Medium Level (Class-Based Factory Method with Inheritance)
#---------------------------------------------------------------------
'''
we move to the "true" GoF structure — 
the factory method is defined in a base Creator class, and subclasses override 
it to decide which product to create.
'''
from abc import ABC, abstractmethod

# Product interface
class Notification(ABC):
    @abstractmethod
    def send(self, message):
        pass


# Concrete Products
class EmailNotification(Notification):
    def send(self, message):
        return f"Sending EMAIL: {message}"


class SMSNotification(Notification):
    def send(self, message):
        return f"Sending SMS: {message}"


class PushNotification(Notification):
    def send(self, message):
        return f"Sending PUSH notification: {message}"


# Creator (abstract) — declares the factory method
class NotificationCreator(ABC):
    @abstractmethod
    def create_notification(self) -> Notification:
        """The factory method — subclasses override this"""
        pass

    def notify(self, message):
        """
        This is the key idea: the Creator's business logic uses the
        product WITHOUT knowing its concrete class.
        """
        notification = self.create_notification()  # 1. Instantiate the product
        return notification.send(message)          # 2. Use the product


# Concrete Creators — each decides WHICH product to instantiate
class EmailNotificationCreator(NotificationCreator):
    def create_notification(self) -> Notification:
        return EmailNotification()


class SMSNotificationCreator(NotificationCreator):
    def create_notification(self) -> Notification:
        return SMSNotification()


class PushNotificationCreator(NotificationCreator):
    def create_notification(self) -> Notification:
        return PushNotification()


# Usage
def send_alert(creator: NotificationCreator, message: str):
    print(creator.notify(message))


send_alert(EmailNotificationCreator(), "Server is down!")
send_alert(SMSNotificationCreator(), "OTP: 4521")
send_alert(PushNotificationCreator(), "New message received")

'''
1. What are we trying to achieve? (The "Point")
In a real application (like an alert system), you want a common function like send_alert() to send messages without hardcoding if channel == "email": ... elif channel == "sms": ....
The Gang of Four (GoF) Factory Method pattern solves this by separating two things:
What to create (decided by subclasses like EmailNotificationCreator).
How to use it (handled by the base class logic notify()).
By doing this, if you add a new channel in the future (like Slack), you never have to modify the core business logic (notify() or send_alert()). You just add a new subclass.

2. The Code Structure (The 2 Hierarchies)
notice that the code creates two separate parallel families of classes:

Hierarchy A: The Products (What gets created)
Notification (Abstract): The common contract. Guarantees every product has a .send(message) method.
EmailNotification, SMSNotification, PushNotification: Concrete implementations that define how each message is actually sent.

Hierarchy B: The Creators (Who creates the products)
NotificationCreator (Abstract Base Class):
Has an abstract method: create_notification(). This is the Factory Method.
Has fixed business logic: notify(message).
EmailNotificationCreator, SMSNotificationCreator, PushNotificationCreator: Concrete subclasses that override create_notification() to return their specific Product.

3. Step-by-Step Execution Flow
send_alert(EmailNotificationCreator(), "Server is down!")

Here is the exact sequence of execution:

[1] User calls send_alert(creator, message)
      │
      ▼
[2] send_alert invokes creator.notify("Server is down!")
      │
      ▼
[3] Inside NotificationCreator.notify():
    - It calls self.create_notification()  <-- (The Factory Method!)
      │
      ▼
[4] Python dynamically resolves self.create_notification():
    - Because 'creator' is an EmailNotificationCreator, 
      it executes EmailNotificationCreator.create_notification()
    - Returns a new EmailNotification object instance.
      │
      ▼
[5] Back inside notify():
    - 'notification' variable now holds the EmailNotification instance.
    - Calls notification.send("Server is down!")
      │
      ▼
[6] EmailNotification.send() executes:
    - Returns "Sending EMAIL: Server is down!"

notify() has no idea whether notification is an EmailNotification, an SMSNotification, or a PushNotification. It only knows:
"Whatever create_notification() gives me, it will have a .send() method."
This is Polymorphism + Factory Method working together. 
The base class handles the process workflow (notify), while subclasses customize the object creation step (create_notification).

Element                     Role in the Pattern,        Purpose
Notification,               Abstract Product,           Defines what every notification can do (send).
EmailNotification,          Concrete Product,           Implements the actual email delivery.
NotificationCreator,        Abstract Creator,           Houses the business workflow (notify).
create_notification(),      The Factory Method,         Subclasses override this to decide which object to instantiate.
EmailNotificationCreator,   Concrete Creator,           Binds EmailNotification to the factory logic.

'''

#---------------------------------------------------------------------------------
#   Example 3: Hard / Complex Level (Registry-Based Dynamic Factory — Industry Pattern)
#--------------------------------------------------------------------------------- 
'''
This is how large-scale frameworks (e.g., plugin systems, ORMs, payment gateway SDKs) 
implement factories: using a registration mechanism so new product types can be plugged in 
dynamically, even from external modules, without modifying the factory's source code at all.
'''

from abc import ABC, abstractmethod
from typing import Dict, Type


# Product interface
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass

    @abstractmethod
    def refund(self, amount: float) -> str:
        pass


# Concrete Products
class StripeProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> str:
        return f"[Stripe] Charged ${amount:.2f}"

    def refund(self, amount: float) -> str:
        return f"[Stripe] Refunded ${amount:.2f}"


class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> str:
        return f"[PayPal] Charged ${amount:.2f}"

    def refund(self, amount: float) -> str:
        return f"[PayPal] Refunded ${amount:.2f}"


class CryptoProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> str:
        return f"[Crypto] Transferred ${amount:.2f} in BTC equivalent"

    def refund(self, amount: float) -> str:
        return f"[Crypto] Refund not supported — issuing new transfer of ${amount:.2f}"


# Factory with a self-registering mechanism
class PaymentProcessorFactory:
    _registry: Dict[str, Type[PaymentProcessor]] = {}

    @classmethod
    def register(cls, processor_type: str):
        """
        Decorator that lets new processor classes register themselves
        with the factory — no need to edit factory code when adding new types.
        """
        def decorator(processor_cls: Type[PaymentProcessor]):
            cls._registry[processor_type] = processor_cls
            return processor_cls
        return decorator

    @classmethod
    def create_processor(cls, processor_type: str, **kwargs) -> PaymentProcessor:
        processor_cls = cls._registry.get(processor_type)
        if processor_cls is None:
            raise ValueError(
                f"No processor registered for type '{processor_type}'. "
                f"Available: {list(cls._registry.keys())}"
            )
        return processor_cls(**kwargs)


# Register concrete processors using the decorator (this could live in separate plugin files!)
PaymentProcessorFactory.register("stripe")(StripeProcessor)
PaymentProcessorFactory.register("paypal")(PayPalProcessor)
PaymentProcessorFactory.register("crypto")(CryptoProcessor)


# --- Usage ---
def checkout(processor_type: str, amount: float):
    processor = PaymentProcessorFactory.create_processor(processor_type)
    print(processor.process_payment(amount))


checkout("stripe", 49.99)
checkout("paypal", 19.99)
checkout("crypto", 100.00)

# Simulating a NEW payment method added later, from a "plugin" —
# notice PaymentProcessorFactory class itself is NEVER modified
@PaymentProcessorFactory.register("applepay")
class ApplePayProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> str:
        return f"[ApplePay] Charged ${amount:.2f}"

    def refund(self, amount: float) -> str:
        return f"[ApplePay] Refunded ${amount:.2f}"


checkout("applepay", 75.00)  # Works immediately — zero changes to factory code

# Attempting an unregistered type
try:
    checkout("bitcoin_cash", 10.00)
except ValueError as e:
    print(f"Error: {e}")


'''
1. What are we trying to achieve? (The "Point")
In traditional factory setups (like Easy or Medium levels):
An if/elif/else factory requires you to edit the factory file every time a new feature/payment method is added.
A class-inheritance factory requires creating new Creator subclasses every time

The Industry Problem:
What if you are building an enterprise framework, a payment SDK, or a plugin system 
(like Django, pytest, or Stripe)? Third-party developers might want to add their own 
custom payment methods from an external module or plugin without ever touching your framework's core factory code.
The Goal of Example 3:
Build a factory that auto-registers new products dynamically using a Python decorator 
(@register), so the factory automatically learns about new classes without modifying a single
 line of the factory's source code (the ultimate expression of the Open/Closed Principle).

 2. The Mechanics: How the Code Works
The system consists of three main parts:
PaymentProcessorFactory._registry: A dictionary that maps string names to class objects (e.g., {"stripe": StripeProcessor, "paypal": PayPalProcessor}).
@PaymentProcessorFactory.register("key"): A decorator method that takes a class and saves it into _registry.
PaymentProcessorFactory.create_processor("key"): A lookup function that finds the class in _registry, instantiates it, and returns it.

3. Visual Flowchart Diagram
                    ┌───────────────────────────────────────────────┐
                    │ STEP 1: Python loads & executes @register     │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Decorator executes:                           │
                    │ cls._registry["stripe"] = StripeProcessor     │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
┌───────────────────────────────────────────────────────────────────────────────────────┐
│ RESULT: Factory Registry Dictionary = {'stripe': StripeProcessor, 'paypal': ...}     │
└───────────────────────────────────────────┬───────────────────────────────────────────┘
                                            │
                                            │ (Later during program execution)
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ STEP 2: Client calls checkout("stripe", 49.99)│
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Calls PaymentProcessorFactory                 │
                    │       .create_processor("stripe")             │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Looks up "stripe" in _registry dictionary     │
                    └───────────────────────┬───────────────────────┘
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     │                                             │
         [Found in Registry]                                [Not Found]
                     │                                             │
                     ▼                                             ▼
┌──────────────────────────────────────────┐     ┌───────────────────────────────────┐
│ Returns StripeProcessor Class Blueprint  │     │ Raises ValueError("No processor   │
└────────────────────┬─────────────────────┘     │ registered for 'bitcoin_cash'")   │
                     │                           └───────────────────────────────────┘
                     ▼
┌──────────────────────────────────────────┐
│ Instantiates: StripeProcessor()          │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│ Returns instance back to checkout()      │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│ Calls processor.process_payment(49.99)   │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│ Prints: "[Stripe] Charged $49.99"        │
└──────────────────────────────────────────┘


2. Text Walkthrough of the ConnectionsPhase 
Phase 1: Registration (Module Loading Time)
- @PaymentProcessorFactory.register("stripe")   
    Executes the decorator function before any business code runs.
- cls._registry["stripe"] = StripeProcessor
    Stores the class pointer directly in the factory's dictionary _registry.

Phase 2: Factory Request (Runtime)
- checkout("stripe", 49.99)
    Passes "stripe" to PaymentProcessorFactory.create_processor("stripe").
- _registry.get("stripe")
    Retrieves StripeProcessor class object from memory.
- processor_cls(**kwargs)
    Constructs StripeProcessor() object and returns it to checkout().
    
Phase 3: Execution
- processor.process_payment(49.99)
    Executes StripeProcessor.process_payment() and prints the formatted response.

'''