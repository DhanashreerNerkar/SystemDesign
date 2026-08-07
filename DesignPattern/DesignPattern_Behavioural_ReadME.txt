Behavioral Patterns : Deal with communication and responsibility between objects
******************************************************************************

Pattern	Purpose
**************************
-Chain of Responsibility : Passes a request along a chain of handlers
*Command                 : Encapsulates a request as an object
-Interpreter	         : Defines a grammar and interpreter for a language
-Iterator                : Provides a way to access elements of a collection sequentially
-Mediator                : Defines an object that encapsulates how a set of objects interact
-Memento                 : Captures and restores an object's internal state
*Observer                : Defines a one-to-many dependency so dependents get notified of changes
-State                   : Allows an object to alter its behavior when its internal state changes
*Strategy                : Defines a family of interchangeable algorithms
-Template Method         : Defines the skeleton of an algorithm, letting subclasses override steps
-Visitor                 : Separates an algorithm from the object structure it operates on



*********************************Observer Pattern************************************
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

*********************************Stratergy Pattern************************************
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

*************Decorator Pattern*******************
The Decorator Pattern lets you attach new behavior to an object dynamically, by wrapping it inside another object that shares the same interface, instead of modifying the original class or creating a rigid subclass hierarchy.
Each decorator wraps the "core" object (or another decorator), adds its own logic before/after delegating to the wrapped object, and remains fully interchangeable with the original interface. This means behaviors can be stacked in any combination, at runtime, without touching the base class. It solves the problem of "class explosion" — where you'd otherwise need a separate subclass for every combination of features (e.g., EncryptedLoggedCachedProcessor). Decorators follow the Open/Closed Principle: you extend functionality by adding new wrapper classes, not editing existing ones.

Real-time scenario in your system:
When a patient submits demographic data (from registration + lab-report platform), the data needs to pass through several optional, stackable steps before it's stored: PII encryption, audit logging, schema validation, and caching for fast chatbot lookups. Not every downstream consumer needs all four — the raw prediction model pipeline might skip caching, while the patient-facing chatbot API needs caching + validation but not raw audit logging duplicated.
When to use in complex real dev scenarios:

Adding cross-cutting concerns (encryption, logging, rate-limiting, caching) to data pipelines without bloating the core class
Feature-flagging behaviors per environment (e.g., extra validation only in staging)
Middleware chains in APIs (auth → logging → compression → response)

*************Command Pattern*******************
The Command Pattern turns a request or action into a standalone object, instead of calling a method directly. That object holds everything needed to perform the action later — what to do, and on what data — so it can be queued, logged, delayed, retried, or undone. The key idea is separating "who wants something done" from "who actually does it" — the requester just creates and hands off a command object; it doesn't need to know how the action gets executed. This is essential for background jobs, task queues, and workflows where actions don't happen instantly or need to survive a crash and retry later. It also enables undo/redo — since each command is an object, you can store a history of them and reverse the last one. Think of it like writing a to-do note instead of doing the task yourself right now — the note (command) can sit in a queue, get picked up by someone else, retried if it fails, or crossed out (undone).
Real IT scenario: A CI/CD pipeline where each step (build, test, deploy, notify) is a Command object pushed onto a queue — allowing retries on failure, logging of every step, and reordering the pipeline without touching the runner's core code.
Simple everyday example: A restaurant order slip. The waiter (client) writes the order (command) and hands it to the kitchen (invoker/receiver) — the waiter doesn't cook it themselves, and the slip can sit in a queue until a chef is free.
When/where to use it: When a patient completes registration, several things need to happen: send a welcome email, sync their Apple Health data, trigger the prediction model to generate a baseline risk score, and store demographics from the lab-report platform. These are slow, can fail independently (the wearable API might be down), and need retry logic — you don't want registration to fail just because the wearable sync timed out. Each action becomes a Command object pushed to a task queue (e.g., Celery/RabbitMQ), so failures are isolated, retryable, and logged individually.
