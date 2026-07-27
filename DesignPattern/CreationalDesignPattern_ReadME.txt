creational design pattern
*************************
1. Singleton pattern
- ensures a class has only one instance throughout the application's lifetime
- provides a global point of access to that instance.
- no matter how many times you try to create an object of that class, you keep getting back the same object — not a new one.
- Real-Time Software Scenario :Consider a database connection pool manager in an application.
    Opening a database connection is expensive (time + memory).
    If every part of your app created its own connection object, you'd end up with hundreds of redundant connections, exhausting resources.
    Instead, you want one connection manager that the entire app shares.
- Use Singleton when:
    Exactly one instance of a class is needed to coordinate actions across the system.
    That instance needs to be accessible globally.
    Creating multiple instances would cause inconsistent state, resource conflicts, or wasted resources.
- Industry-Level Usage Examples
    Logging systems (e.g., Python's logging module)	- You want all parts of the app writing to the same log file/stream, not each creating separate log handlers
    Configuration managers - App-wide settings (API keys, environment variables) should be loaded once and shared
    Database connection pools (e.g., SQLAlchemy engine)	- Avoid the overhead of repeatedly opening/closing connections
    Caching layers (e.g., Redis client instance) -	One shared cache client avoids redundant connections
    Hardware interface access (e.g., printer spooler, GPU context managers)	- Only one process should control the hardware resource at a time
    Thread pools / Task schedulers (e.g., Celery, Airflow schedulers)	- Centralized coordination of tasks across the app
- Word of caution used in real teams: 
    Singleton is sometimes criticized as an anti-pattern when overused, 
    because it introduces global state, which makes unit testing harder (hard to mock/reset) 
    and can hide dependencies. Senior engineers often prefer dependency injection over 
    Singleton in large systems — but it's still very common in logging, config, and 
    connection-pooling scenarios.
****************************************************************************
2. Factory pattern
- Is a creational design pattern that provides an interface for creating objects, but lets subclasses decide which specific class to instantiate.
- Instead of calling a class constructor directly (SomeClass()), you call a factory method that returns the object for you. The calling code doesn't need to know the exact class being created — it just knows it's getting "a product" that follows a common interface.
- Real-Time Software Scenario
    Consider a document editor application (like Word or Google Docs) that supports exporting to PDF, Word, and HTML formats:
    The "Export" button doesn't want to know the internal details of PDFExporter, WordExporter, or HTMLExporter.
    Instead, it calls a factory method like create_exporter(format_type), which returns the correct exporter object.
    If a new format (e.g., Markdown) is added later, you only extend the factory — the rest of the code stays untouched. 
- Where and When to Use Factory Method:
when to use:
    A class can't anticipate the type of objects it needs to create ahead of time.
    You want to delegate the responsibility of instantiation to subclasses or a centralized creation method.
    You want to decouple client code from concrete classes, so adding new types doesn't break existing code (Open/Closed Principle).
    Object creation involves complex logic (e.g., choosing between multiple related classes based on configuration, input, or environment).
-Industry-Level Usage Examples
Industry Use Case	                                    Why Factory Method?
UI toolkits (e.g., cross-platform GUI frameworks)	    Create the right button/widget for Windows, Mac, or Linux without the app logic knowing OS-specific details
Database drivers (e.g., SQLAlchemy, Django ORM)	        create_connection() returns a MySQL, PostgreSQL, or SQLite connection object depending on config
Payment gateways (e.g., Stripe, PayPal integrations)    create_payment_processor(type) returns the correct processor without checkout code knowing implementation details
Logging frameworks	                                    Factory returns a FileLogger, ConsoleLogger, or CloudLogger based on environment settings
Notification systems	                                create_notifier(channel) returns an EmailNotifier, SMSNotifier, or PushNotifier
Game development	                                    Spawning different enemy/character types based on level or difficulty, without hardcoding each type into the game engine
- Industry insight: 
    Factory Method is one of the most heavily used patterns in real frameworks 
    because it directly supports the Open/Closed Principle — you can add new p
    roduct types without modifying existing factory-calling code, only by 
    extending the factory itself.