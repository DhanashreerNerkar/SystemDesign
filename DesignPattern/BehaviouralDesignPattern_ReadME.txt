Behavioural design pattern
*************************
1. Stratergy pattern
_____________________
- Strategy Pattern is a behavioral design pattern that defines a family of interchangeable 
    algorithms, encapsulates each one separately, and allows the algorithm to be swapped at runtime 
    without changing the client code that uses it.
- In simpler terms: instead of hardcoding "if this condition, do algorithm A; else do algorithm 
    B" inside a class, you extract each algorithm into its own class (a "strategy"), 
    and the main class just holds a reference to whichever strategy it's currently using. 
    You can swap strategies in and out like plugging in different tools for the same job.
- Real-World Scenario (Non-Technical)   
    Think of navigation apps like Google Maps. When you ask for directions, you can choose: 
    "Driving," "Walking," "Cycling," or "Public Transit." Each mode calculates the route using 
    a completely different algorithm (roads vs. footpaths vs. bus schedules), but the interface 
    stays the same — you press "Get Directions" and get a route back. The app doesn't rewrite 
    its core logic for each mode; it just plugs in a different strategy.
- Real-Time Software Scenario
    Consider an e-commerce checkout system that calculates shipping cost:
    Standard shipping, Express shipping, and International shipping all calculate cost differently 
    (flat rate vs. weight-based vs. distance + customs). Instead of a giant if/elif block 
    inside the Order class, each shipping method becomes its own strategy class. The checkout 
    page can switch strategies based on what the customer selects — and adding a new shipping 
    method later doesn't touch the Order class at all.
- Use Strategy when:
    You have multiple ways to perform the same task, and you want to switch between them 
    dynamically at runtime. You want to avoid conditional complexity — long if/elif/else or 
    switch chains that pick behavior based on type/flag. Different variants of an algorithm 
    need to be interchangeable, and each variant should be independently testable and extendable.
    You want to follow the Open/Closed Principle — adding a new algorithm shouldn't require 
    modifying existing code, just adding a new strategy class.
- Industry-Level Usage Examples
Industry Use Case	                    Why Strategy?
    Payment processing	                Choosing between Credit Card, PayPal, Crypto payment 
                                        validation/processing logic at checkout
    Sorting/searching libraries	        Passing a custom comparator function 
                                        (Python's sorted(key=...) is essentially Strategy)
    Compression tools	                Switching between ZIP, GZIP, or LZ4 compression 
                                        algorithms based on file type
    Route optimization 	                Different route-calculation strategies 
                                        (fastest, cheapest, fewest stops)
    / logistics (e.g., Uber, FedEx)     Swapping between OAuth, JWT, Basic Auth strategies 
                                        without changing the login controller
    Authentication systems	
    Game AI	Different enemy behavior    strategies (aggressive, defensive, passive) that can 
                                        change dynamically during gameplay
    Pricing engines (e-commerce)	    Discount strategies: seasonal sale, loyalty discount,
                                        bulk discount — swappable per promotion
- Industry insight: Strategy is one of the most common patterns hiding in plain sight in 
    Python — anytime you pass a function as an argument (like sorted(data, key=my_func) or 
    map(func, list)), you're using the Strategy pattern conceptually, since Python's 
    first-class functions make it lightweight to implement.

2. Observer pattern
_______________________
Observer Pattern is a behavioral design pattern that defines a one-to-many dependency 
between objects: when one object (the Subject, sometimes called "Publisher" or "Observable") 
changes state, all its dependents (the Observers, sometimes called "Subscribers") are 
automatically notified and updated — without the Subject needing to know any details about 
who its observers are or what they'll do with the notification.

Real-World Scenario (Non-Technical)
Think of YouTube channel subscriptions. The channel (Subject) doesn't know or care who's 
subscribed or what they'll do when it uploads. It just uploads a video, and every subscriber 
(Observer) gets notified automatically. Subscribers can join or leave anytime, and the 
channel's upload process never changes because of that.

Real-Time Software Scenario
Consider a stock trading platform: A Stock object holds the live price of "AAPL."
Multiple parts of the system care about price changes: a mobile app UI that needs to 
refresh the displayed price, a trading bot that needs to trigger buy/sell logic, and a 
logging service that records price history for auditing. Instead of the Stock class 
hardcoding calls to the UI, the bot, and the logger (which would tightly couple everything), 
it just maintains a list of observers and notifies them all when the price changes. 
New observers (e.g., an SMS alert system) can be added later with zero changes to the Stock class.

Where and When to Use Observer Pattern
Use Observer when: A change in one object requires changing others, and you don't know 
(or don't want to hardcode) how many objects need to react. You want loose coupling between 
the object that holds state and the objects that react to state changes. You need to support 
broadcast communication — one event, many independent reactions. The set of interested 
parties can change dynamically at runtime (subscribe/unsubscribe).

Industry-Level Usage Examples
Industry-Level Usage Examples
GUI Frameworks (e.g., Tkinter, Qt, React state)

Why Observer? Widgets/components re-render automatically when underlying data changes.
Event-Driven Systems (e.g., Node.js EventEmitter, Python's asyncio events)
Why Observer? Multiple handlers react to the same event (user login, file upload, etc.).

Model-View Architectures (MVC/MVVM)
Why Observer? Views automatically update when the Model's data changes, without the Model 
knowing about the Views.

Pub/Sub Messaging Systems (e.g., Kafka, RabbitMQ, Redis Pub/Sub)
Why Observer? Large-scale, distributed version of Observer — publishers broadcast, 
many subscribers consume independently.

Reactive Programming Libraries (e.g., RxPY, RxJS)
Why Observer? Streams of data notify all subscribed operators/consumers.

Real-Time Dashboards (e.g., stock tickers, sports scores, IoT sensor monitoring)
Why Observer? Multiple display components update simultaneously when new data arrives.

Version Control Systems (e.g., Git hooks, CI/CD pipelines)
Why Observer? Multiple automated processes (tests, deployments, notifications) trigger when 
a commit/push event happens.