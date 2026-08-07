#Example 1: Easy Level (Basic Observer)
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def updates(self, temperature):
        pass

class Phonedisplay(Observer):
    def updates(self,temperature):
        print("phone temp:{temperature}C")

class Windowdisplay(Observer):
    print("win temp:{temperature}C")

class WeatherStation:
    def __init__(self):
        self.observers=[]
        self.temperature=0

    def subscribe(self,observer:Observer):
        self.observers.append(observer) 

    def unsubscribe(self,observer:Observer):
        self.observers.remove(observer) 

    def set_temperature(self,temperature):
        self._temperature=temperature
        self._notify_all()

    def _notify_all(self):
        for observer in self.observers:
            self.observers(self._temperature)

station=WeatherStation()
phone=Phonedisplay()
window=Windowdisplay()

station.subscribe(phone)
station.subscribe(window)

station.set_temperature(25)
# [Phone Display] Temperature updated: 25°C
# [Window Display] Temperature updated: 25°C
station.unsubscribe(window)
station.set_temperature(35)
# [Phone Display] Temperature updated: 30°C   <- window no longer notified

#***********************
# Example 2: 
# Medium Level (Observer with Event Types + Push/Pull Data Model)
#************************
'''
Real systems often need multiple kinds of events, and observers may want different pieces of 
data (not just one value). This example introduces an event object instead of a raw value, 
and shows the difference between "push" (Subject sends data) and "pull" (Observer requests 
data) models.
'''

from abc import ABC,abstractmethod
from dataclasses import dataclass

class EventType(Enum):
    PRICE_CHANGE="price_change"
    VOLUME_SPIKE="volume_spike"

@dataclass
class StockEvent:
    event_type:EventType
    symbol:str
    old_value:float
    new_value:float

class StockObserver(ABC):
    @abstractmethod
    def on_event(self,event:StockEvent):
        pass
# Concrete Observers — each reacts differently, and only to events it cares about
class TradingBot(StockObserver):
    def __init__(self, threshold_percent=5.0):
        self.threshold_percent = threshold_percent

    def on_event(self, event: StockEvent):
        if event.event_type == EventType.PRICE_CHANGE:
            change_pct = ((event.new_value - event.old_value) / event.old_value) * 100
            if change_pct >= self.threshold_percent:
                print(f"[TradingBot] {event.symbol} jumped {change_pct:.1f}% -> Triggering BUY logic")
            elif change_pct <= -self.threshold_percent:
                print(f"[TradingBot] {event.symbol} dropped {change_pct:.1f}% -> Triggering SELL logic")


class PriceLogger(StockObserver):
    def __init__(self):
        self.history: List[StockEvent] = []

    def on_event(self, event: StockEvent):
        self.history.append(event)
        print(f"[Logger] Recorded: {event.symbol} {event.event_type.value} "
              f"{event.old_value} -> {event.new_value}")


class MobileAppUI(StockObserver):
    def on_event(self, event: StockEvent):
        if event.event_type == EventType.PRICE_CHANGE:
            print(f"[Mobile UI] Refreshing display for {event.symbol}: ${event.new_value}")


class Stock:
    def __init__(self,symbol:str,price:float):
        self.symbol=symbol
        self._price=price
        self._observers:List[StockObserver]=[]

    def subscribe(self,observer:StockObserver):
        self._observers.append(observer)

    def unsubscribe(self,observer:StockObserver):
            self._observers.remove(observer)

    def set_price(self,new_price:float):
        old_price=self._price
        self._price=new_price
        event=StockEvent(
            event_type=EventType.PRICE_CHANGE,
            symbol=self.symbol,
            old_value=old_price,
            new_price=new_price
        )
        self._notify(event)

    def _notify(self,event:StockEvent):
        for observer in self._observers:
            observer.on_event(event)

apple_stock=Stock("APPL",150.0)
bot = TradingBot(threshold_percent=3.0)
logger = PriceLogger()
ui = MobileAppUI()

apple_stock.subscribe(bot)
apple_stock.subscribe(logger)
apple_stock.subscribe(ui)

apple_stock.set_price(160.0)  # +6.7% -> triggers bot's BUY logic
print("---")
apple_stock.set_price(158.0)  

'''
Example 3: 
Hard / Complex Level (Thread-Safe, Weak-Reference, Multi-Event Observer System — Industry Pattern)
'''
'''
closer to how production event systems (e.g., internal pub/sub used inside frameworks, or 
something like Django signals / Qt signals) are actually built: supporting multiple event 
channels, weak references (to avoid memory leaks from forgotten unsubscribes), and thread 
safety.
'''

import threading
import weakref
from typing import Callable, Dict, List, Any
from dataclasses import dataclass, field
from enum import Enum
import time


class ChannelType(Enum):
    ORDER_CREATED = "order_created"
    ORDER_SHIPPED = "order_shipped"
    ORDER_CANCELLED = "order_cancelled"


@dataclass
class Event:
    channel: ChannelType
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)


class EventBus:
    """
    A production-style Subject that supports:
    - Multiple named channels (event types)
    - Weak references to observers (prevents memory leaks if subscriber
      forgets to unsubscribe — a REAL bug that happens in long-running apps)
    - Thread-safe subscribe/notify (multiple threads may publish/subscribe concurrently)
    - Exception isolation (one broken observer shouldn't crash others)
    """

    def __init__(self):
        self._subscribers: Dict[ChannelType, List[weakref.ref]] = {}
        self._lock = threading.RLock()

    def subscribe(self, channel: ChannelType, callback: Callable[[Event], None]):
        with self._lock:
            if channel not in self._subscribers:
                self._subscribers[channel] = []

            # Use a weak reference so if the subscriber object is garbage collected
            # (e.g., a UI component that was destroyed), it's automatically cleaned up
            # instead of causing a memory leak or a crash calling a dead object.
            if hasattr(callback, '__self__'):  # bound method
                ref = weakref.WeakMethod(callback)
            else:
                ref = weakref.ref(callback)

            self._subscribers[channel].append(ref)

    def unsubscribe(self, channel: ChannelType, callback: Callable):
        with self._lock:
            if channel in self._subscribers:
                self._subscribers[channel] = [
                    ref for ref in self._subscribers[channel]
                    if ref() is not None and ref() != callback
                ]

    def publish(self, event: Event):
        with self._lock:
            subscribers = self._subscribers.get(event.channel, [])
            # Clean up dead references while iterating
            alive_refs = []
            callbacks_to_call = []

            for ref in subscribers:
                callback = ref()
                if callback is not None:
                    alive_refs.append(ref)
                    callbacks_to_call.append(callback)

            self._subscribers[event.channel] = alive_refs  # Prune dead refs

        # Call callbacks OUTSIDE the lock to avoid deadlocks if a callback
        # tries to subscribe/publish again (re-entrancy)
        for callback in callbacks_to_call:
            try:
                callback(event)
            except Exception as e:
                # Exception isolation: one bad observer doesn't kill the notification
                # loop for everyone else — critical in production systems
                print(f"[EventBus] Observer raised an error, isolated: {e}")


# --- Concrete subscriber services ---

class InventoryService:
    def __init__(self, bus: EventBus):
        bus.subscribe(ChannelType.ORDER_CREATED, self.reserve_stock)
        bus.subscribe(ChannelType.ORDER_CANCELLED, self.release_stock)

    def reserve_stock(self, event: Event):
        print(f"[Inventory] Reserving stock for order {event.payload['order_id']}")

    def release_stock(self, event: Event):
        print(f"[Inventory] Releasing stock for cancelled order {event.payload['order_id']}")


class EmailService:
    def __init__(self, bus: EventBus):
        bus.subscribe(ChannelType.ORDER_CREATED, self.send_confirmation)
        bus.subscribe(ChannelType.ORDER_SHIPPED, self.send_shipping_notice)

    def send_confirmation(self, event: Event):
        print(f"[Email] Sending confirmation for order {event.payload['order_id']} "
              f"to {event.payload['customer_email']}")

    def send_shipping_notice(self, event: Event):
        print(f"[Email] Sending shipping notice for order {event.payload['order_id']}")


class AnalyticsService:
    def __init__(self, bus: EventBus):
        for channel in ChannelType:
            bus.subscribe(channel, self.track_event)  # Subscribes to ALL channels
        self.event_count = 0

    def track_event(self, event: Event):
        self.event_count += 1
        print(f"[Analytics] Tracked event #{self.event_count}: {event.channel.value}")


class BuggyObserver:
    """Simulates a real bug — this observer crashes on every event"""
    def __init__(self, bus: EventBus):
        bus.subscribe(ChannelType.ORDER_CREATED, self.handle)

    def handle(self, event: Event):
        raise RuntimeError("Simulated bug in a subscriber!")


# --- Usage ---
bus = EventBus()

inventory = InventoryService(bus)
email = EmailService(bus)
analytics = AnalyticsService(bus)
buggy = BuggyObserver(bus)  # This one will throw errors, but shouldn't break the others

print("=== Publishing ORDER_CREATED ===")
bus.publish(Event(
    channel=ChannelType.ORDER_CREATED,
    payload={"order_id": "ORD-123", "customer_email": "user@example.com"}
))

print("\n=== Publishing ORDER_SHIPPED ===")
bus.publish(Event(
    channel=ChannelType.ORDER_SHIPPED,
    payload={"order_id": "ORD-123"}
))

print("\n=== Publishing ORDER_CANCELLED ===")
bus.publish(Event(
    channel=ChannelType.ORDER_CANCELLED,
    payload={"order_id": "ORD-124"}
))

print(f"\nTotal events tracked by Analytics: {analytics.event_count}")

'''
Central Idea
EventBus = A phone switchboard operator. It doesn't call anyone directly — it just connects "callers" (publishers) to whoever's "listening" on a given line (channel), and it doesn't care what happens on the call.

🌿 Branch 1: WHO'S TALKING TO WHOM
Think of it as 3 layers, top to bottom:
Event          →  the actual "message" (what happened + data)
Channel        →  the "topic" the message belongs to (like a radio frequency)
Subscriber     →  anyone tuned into that frequency

Analogy: A radio station.
ChannelType.ORDER_CREATED = 91.5 FM
Event = the song currently playing
InventoryService, EmailService = people who tuned their radio to 91.5 FM
bus.publish() = the station broadcasting

That's it — that's 80% of the code's purpose. Everything else is just making the broadcast safe and reliable.

🌿 Branch 2: THE 4 PROBLEMS THIS CODE SOLVES

Instead of reading line-by-line, memorize it as 4 real-world problems + their 1-line fix:
#	Real Problem	Fix in Code	One-line "why"
1	"What if a subscriber forgets to unsubscribe and gets deleted?"	weakref.ref() / weakref.WeakMethod()	Dead subscribers vanish automatically instead of leaking memory forever
2	"What if two threads publish/subscribe at the same time?"	threading.RLock()	Only one thread touches the subscriber list at once
3	"What if one subscriber crashes?"	try/except around each callback	The crash is caged — it doesn't kill notifications to everyone else
4	"What if a callback tries to publish/subscribe again while running?"	Lock released before calling callbacks	Prevents a deadlock (self-strangling the lock)

Memory trick: Leak → Race → Crash → Deadlock — the 4 classic bugs in any notification system, in the order a junior dev usually discovers them the hard way.

🌿 Branch 3: THE LIFECYCLE OF ONE publish() CALL
Picture it as a 3-step pipeline, like a bouncer checking a guest list:
STEP 1: LOCK the guest list          (thread safety)
   ↓
STEP 2: CHECK who's still alive      (weakref cleanup — remove ghosts)
   ↓
STEP 3: UNLOCK, then knock on each door (call callbacks — outside the lock!)
   ↓
   If a door doesn't open (exception) → shrug, move to next door

The key visual: the lock is only around "reading the list," never around "calling the people." That separation is the single most important design decision in this whole example.

🌿 Branch 4: THE CAST OF CHARACTERS
Draw this as a simple hub-and-spoke diagram in your head:

                    EventBus (the hub)
                    /      |      \
                   /       |       \
          Inventory     Email    Analytics    (+ Buggy)
          (listens to    (listens  (listens to
           2 channels)   to 2)     ALL channels)

           InventoryService — reacts to ORDER_CREATED and ORDER_CANCELLED only
EmailService — reacts to ORDER_CREATED and ORDER_SHIPPED only
AnalyticsService — reacts to everything (subscribes in a loop over all ChannelTypes) — this is your "counts all traffic" service
BuggyObserver — the intentional saboteur, proving Problem #3 (Crash isolation) actually works
🧠 The One-Sentence Summary to Lock It In

"A central switchboard keeps a list of who's listening to what, cleans out dead listeners automatically, hands out notifications one at a time without holding a lock, and shrugs off any listener that misbehaves — so nobody can break anyone else."

If you can redraw the hub-and-spoke diagram from Branch 4 and explain why each of the 4 fixes in Branch 2 exists, you've internalized the hard example without needing to re-read the code.
'''