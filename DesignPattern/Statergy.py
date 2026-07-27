#------------------------------------------------------------------------------
#Example 1: Easy Level (Basic Strategy with Classes)
#A simple example: calculating discounts differently based on customer type.
#------------------------------------------------------------------------------
from abc import ABC, abstractmethod

# Strategy interface
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, price):
        pass


# Concrete Strategies
class NoDiscount(DiscountStrategy):
    def apply_discount(self, price):
        return price


class StudentDiscount(DiscountStrategy):
    def apply_discount(self, price):
        return price * 0.9  # 10% off


class PremiumMemberDiscount(DiscountStrategy):
    def apply_discount(self, price):
        return price * 0.75  # 25% off


# Context — uses a strategy but doesn't care which one
class ShoppingCart:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def checkout(self, price):
        return self.strategy.apply_discount(price)


# Usage
cart1 = ShoppingCart(NoDiscount())
cart2 = ShoppingCart(StudentDiscount())
cart3 = ShoppingCart(PremiumMemberDiscount())

print(cart1.checkout(100))  # 100
print(cart2.checkout(100))  # 90.0
print(cart3.checkout(100))  # 75.0

#---------------------------------------------------------------------------------------
# Example 2: Medium Level (Strategy with Runtime Switching + Function-Based Strategies)
# Real systems often need to change strategy after the object is created (not just at 
# construction time), and Python lets us use functions directly as strategies instead of 
# always requiring full classes — this is more "Pythonic."
#---------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import Callable


# Strategy interface (class-based, for complex strategies)
class RouteStrategy(ABC):
    @abstractmethod
    def calculate_route(self, start, end):
        pass


class DrivingStrategy(RouteStrategy):
    def calculate_route(self, start, end):
        return f"Driving route from {start} to {end}: 15 km via highway"


class WalkingStrategy(RouteStrategy):
    def calculate_route(self, start, end):
        return f"Walking route from {start} to {end}: 3 km via footpaths"


class PublicTransitStrategy(RouteStrategy):
    def calculate_route(self, start, end):
        return f"Transit route from {start} to {end}: Bus 42 + Metro Line 3"


# Context — allows swapping strategy dynamically AFTER creation
class NavigationApp:
    def __init__(self, strategy: RouteStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: RouteStrategy):
        """Allows switching the algorithm at runtime"""
        self._strategy = strategy

    def get_directions(self, start, end):
        return self._strategy.calculate_route(start, end)


# --- Usage: runtime switching ---
nav = NavigationApp(DrivingStrategy())
print(nav.get_directions("Home", "Office"))

nav.set_strategy(WalkingStrategy())  # User changes mode mid-session
print(nav.get_directions("Home", "Office"))

nav.set_strategy(PublicTransitStrategy())
print(nav.get_directions("Home", "Office"))


# --- Bonus: Pythonic function-based strategy (no classes needed) ---
def calculate_total_with_tax(price: float, tax_strategy: Callable[[float], float]) -> float:
    return tax_strategy(price)


def us_tax(price):
    return price * 1.07  # 7% sales tax

def eu_vat(price):
    return price * 1.20  # 20% VAT

def tax_free(price):
    return price


print(calculate_total_with_tax(100, us_tax))    # 107.0
print(calculate_total_with_tax(100, eu_vat))     # 120.0
print(calculate_total_with_tax(100, tax_free))   # 100

'''
1. What are we trying to achieve? (The "Point")
In real-world applications, two key requirements often come up:
Runtime Strategy Switching: A user might start a session driving, but mid-trip decide to walk or take public transit. We need our NavigationApp object to dynamically switch algorithms on the fly without recreating the entire app or restarting the session.
Function-Based Strategies (Pythonic Style): In Python, functions are "first-class citizens" (you can pass a function as an argument just like a variable). For simpler algorithms (like calculating tax or discounts), creating full OOP classes with inheritance is overkill. Passing raw functions is much cleaner and faster.

2. Part 1: OOP Strategy with Runtime Switching
    Code Logic & Structure
        RouteStrategy (Abstract Class): Defines the contract (calculate_route(start, end)).
        DrivingStrategy, WalkingStrategy, PublicTransitStrategy: Concrete classes that implement the specific routing logic for each travel mode.
        NavigationApp (Context): Stores a reference to the active strategy in self._strategy.
        The Magic Method: set_strategy()
    
    The key method in NavigationApp is:
        def set_strategy(self, strategy: RouteStrategy):
        self._strategy = strategy
    
    This simple setter method allows you to swap out the underlying algorithm at any point after the NavigationApp object has already been created.

    Step-by-Step Execution Flow (Part 1):
    [1] User creates NavigationApp: nav = NavigationApp(DrivingStrategy())
      │
      ▼
[2] Calls nav.get_directions("Home", "Office")
      │ └── Executes DrivingStrategy.calculate_route()
      │ └── Returns: "Driving route ... 15 km via highway"
      │
      ▼
[3] User switches mode: nav.set_strategy(WalkingStrategy())
      │ └── Replaces self._strategy with WalkingStrategy instance!
      │
      ▼
[4] Calls nav.get_directions("Home", "Office")
      │ └── Executes WalkingStrategy.calculate_route()
      │ └── Returns: "Walking route ... 3 km via footpaths"
      │
      ▼
[5] User switches mode: nav.set_strategy(PublicTransitStrategy())
      │ └── Replaces self._strategy with PublicTransitStrategy instance!
      │
      ▼
[6] Calls nav.get_directions("Home", "Office")
        └── Executes PublicTransitStrategy.calculate_route()
        └── Returns: "Transit route ... Bus 42 + Metro Line 3"

    3. Part 2: Function-Based Strategies ("Pythonic" Style)

    Code Logic: Instead of creating strategy classes, we use standard Python functions:
    def us_tax(price): 
        return price * 1.07  # 7% tax

    def eu_vat(price): 
        return price * 1.20  # 20% VAT

    def tax_free(price): 
        return price

    And the "Context" is simply a function that accepts another function as a parameter:
    def calculate_total_with_tax(price: float, tax_strategy: Callable[[float], float]) -> float:
        return tax_strategy(price)

    Execution Flow (Part 2)
    calculate_total_with_tax(100, us_tax)   ──> Calls us_tax(100)   ──> Returns 107.0
    calculate_total_with_tax(100, eu_vat)   ──> Calls eu_vat(100)   ──> Returns 120.0
    calculate_total_with_tax(100, tax_free) ──> Calls tax_free(100) ──> Returns 100.0

    Why show this? In Python interviews, writing 4 classes for simple strategy calculations 
    can look overly rigid (Java-style). Showing that you know how to pass functions directly 
    (Callable) proves you understand native Python capabilities!

    Concept                     Traditional OOP Strategy,           Pythonic Function Strategy
    Best Used For,              Complex algorithms needing internal state or multiple methods.,"Simple, single-method algorithms (math, string formatting, filters)."
    How Strategy is Passed,     "Object instance (e.g., DrivingStrategy()).","Raw function name (e.g., us_tax)."
    Runtime Switching,          Via a set_strategy() method on the Context object.,By passing a different function argument on each function call.
'''

#------------------------------------------------------------------------------------------
# Example 3: Hard / Complex Level (Strategy + Registry + Context State — Industry Pattern)
# This combines Strategy with a self-registering factory (similar to what we did in Factory 
# Method) plus contextual configuration, mirroring how production systems like pricing engines, 
# shipping calculators, and fraud-detection systems dynamically select and configure strategies based on live data.
# ----------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import Dict, Type, Optional
from dataclasses import dataclass


@dataclass
class ShipmentDetails:
    weight_kg: float
    distance_km: float
    is_international: bool
    declared_value: float


# Strategy interface
class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, details: ShipmentDetails) -> float:
        pass

    @abstractmethod
    def estimated_days(self, details: ShipmentDetails) -> int:
        pass


# Registry-based strategy factory (same self-registering idea as Factory Method)
class ShippingStrategyRegistry:
    _strategies: Dict[str, Type[ShippingStrategy]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(strategy_cls: Type[ShippingStrategy]):
            cls._strategies[name] = strategy_cls
            return strategy_cls
        return decorator

    @classmethod
    def get_strategy(cls, name: str) -> ShippingStrategy:
        strategy_cls = cls._strategies.get(name)
        if strategy_cls is None:
            raise ValueError(f"Unknown shipping strategy: '{name}'. Available: {list(cls._strategies.keys())}")
        return strategy_cls()

    @classmethod
    def recommend_strategy(cls, details: ShipmentDetails) -> str:
        """
        Business logic that picks the BEST strategy automatically
        based on shipment characteristics — this is what real
        logistics systems (FedEx, Amazon) do behind the scenes.
        """
        if details.is_international:
            return "international"
        elif details.weight_kg > 20:
            return "freight"
        elif details.distance_km < 50:
            return "same_day"
        else:
            return "standard"


@ShippingStrategyRegistry.register("standard")
class StandardShipping(ShippingStrategy):
    def calculate_cost(self, details: ShipmentDetails) -> float:
        return 5.0 + (details.weight_kg * 0.5) + (details.distance_km * 0.05)

    def estimated_days(self, details: ShipmentDetails) -> int:
        return 5


@ShippingStrategyRegistry.register("same_day")
class SameDayShipping(ShippingStrategy):
    def calculate_cost(self, details: ShipmentDetails) -> float:
        return 15.0 + (details.weight_kg * 1.2)

    def estimated_days(self, details: ShipmentDetails) -> int:
        return 0  # Same day


@ShippingStrategyRegistry.register("freight")
class FreightShipping(ShippingStrategy):
    def calculate_cost(self, details: ShipmentDetails) -> float:
        return 50.0 + (details.weight_kg * 0.3) + (details.distance_km * 0.02)

    def estimated_days(self, details: ShipmentDetails) -> int:
        return 7


@ShippingStrategyRegistry.register("international")
class InternationalShipping(ShippingStrategy):
    def calculate_cost(self, details: ShipmentDetails) -> float:
        base = 30.0 + (details.weight_kg * 2.0) + (details.distance_km * 0.08)
        customs_fee = details.declared_value * 0.1  # 10% customs
        return base + customs_fee

    def estimated_days(self, details: ShipmentDetails) -> int:
        return 12


# Context — the order/checkout system that USES strategies without knowing internals
class Order:
    def __init__(self, shipment: ShipmentDetails, strategy_name: Optional[str] = None):
        self.shipment = shipment
        # If no strategy explicitly chosen, auto-recommend one based on shipment data
        chosen_strategy = strategy_name or ShippingStrategyRegistry.recommend_strategy(shipment)
        self.strategy: ShippingStrategy = ShippingStrategyRegistry.get_strategy(chosen_strategy)
        self.strategy_name = chosen_strategy

    def get_shipping_summary(self) -> str:
        cost = self.strategy.calculate_cost(self.shipment)
        days = self.strategy.estimated_days(self.shipment)
        return (f"Strategy: {self.strategy_name} | "
                f"Cost: ${cost:.2f} | "
                f"Estimated delivery: {days} day(s)")


# --- Usage ---

# Case 1: Local small package -> auto-recommends "same_day"
order1 = Order(ShipmentDetails(weight_kg=1.5, distance_km=20, is_international=False, declared_value=50))
print(order1.get_shipping_summary())

# Case 2: Heavy package -> auto-recommends "freight"
order2 = Order(ShipmentDetails(weight_kg=35, distance_km=300, is_international=False, declared_value=500))
print(order2.get_shipping_summary())

# Case 3: International package -> auto-recommends "international"
order3 = Order(ShipmentDetails(weight_kg=5, distance_km=8000, is_international=True, declared_value=1200))
print(order3.get_shipping_summary())

# Case 4: Customer manually overrides the recommended strategy
order4 = Order(
    ShipmentDetails(weight_kg=2, distance_km=100, is_international=False, declared_value=80),
    strategy_name="same_day"  # Forces same-day even though it wouldn't normally be recommended
)
print(order4.get_shipping_summary())

# Case 5: New strategy added later (e.g., "eco_friendly") — zero changes to Order class
@ShippingStrategyRegistry.register("eco_friendly")
class EcoFriendlyShipping(ShippingStrategy):
    def calculate_cost(self, details: ShipmentDetails) -> float:
        return 8.0 + (details.weight_kg * 0.4)  # Cheaper, slower, carbon-offset

    def estimated_days(self, details: ShipmentDetails) -> int:
        return 8

order5 = Order(
    ShipmentDetails(weight_kg=3, distance_km=40, is_international=False, declared_value=60),
    strategy_name="eco_friendly"
)
print(order5.get_shipping_summary())

'''
1. What are we trying to achieve? (The "Point")
In a basic Strategy pattern, the client has to manually pick and pass a strategy object (e.g., Order(shipment, StandardShipping())).
However, in production logistics platforms (like Amazon, FedEx, or Shopify):
Automated Intelligence: The system should look at the package details (weight, distance, international flag) and automatically pick the best strategy for the customer.
Dynamic Extensibility: Developers/Plugins should be able to register new shipping strategies (e.g., EcoFriendlyShipping) using a decorator without editing the core Order or Registry classes.
Flexible Context: Calculations need rich data objects (ShipmentDetails), not just single values.
Manual Overrides: The customer can accept the recommended strategy OR manually force a specific strategy (e.g., "Same-Day").
Example 3 combines Strategy Pattern + Factory Pattern + Auto-Selection Engine into one industry-grade system.

2. The Core ComponentsShipmentDetails (Context Data): 
A structured data container (dataclass) holding weight_kg, distance_km, is_international, and
 declared_value.

ShippingStrategy (Strategy Interface): Guarantees every concrete strategy implements 
calculate_cost() and estimated_days().
ShippingStrategyRegistry (Factory & Auto-Selector):
- _strategies: Dictionary mapping strategy names to strategy classes 
    (e.g., "freight" $\rightarrow$ FreightShipping).    
-  @register("name"): Decorator that registers new strategies.  
- recommend_strategy(details): Rule-based engine that automatically chooses the best 
    strategy based on ShipmentDetails.
Order (Client / Context): The order processor that requests a strategy, executes it, and prints the summary.


3. Step-by-Step Code Flow
Here is what happens step-by-step when an order is created:
# Create an order for a heavy package (35 kg, 300 km)
order = Order(ShipmentDetails(weight_kg=35, distance_km=300, is_international=False, declared_value=500))

Visual Execution Flow
[1] Order Object Initialized with ShipmentDetails(weight_kg=35, ...)
      │
      ▼
[2] Did the user provide an explicit strategy name?
      ├── YES ──> Use that strategy name.
      └── NO  ──> Call ShippingStrategyRegistry.recommend_strategy(shipment)
                    │
                    ▼
[3] recommend_strategy() evaluates rules:
      ├── is_international? ──> "international"
      ├── weight > 20 kg?    ──> "freight"  <-- (MATCHED! Returns "freight")
      ├── distance < 50 km?  ──> "same_day"
      └── default            ──> "standard"
                    │
                    ▼
[4] Order calls ShippingStrategyRegistry.get_strategy("freight")
      │ └── Looks up "freight" in _strategies dictionary
      │ └── Instantiates FreightShipping() object
      │
      ▼
[5] Order calls order.get_shipping_summary()
      │
      ├── Calls strategy.calculate_cost(shipment) ──> Calculates cost using Freight formula
      ├── Calls strategy.estimated_days(shipment) ──> Returns 7 days
      │
      ▼
[6] Returns formatted summary:
    "Strategy: freight | Cost: $66.50 | Estimated delivery: 7 day(s)"

4. What happens when a new strategy is added?
The @register("eco_friendly") decorator immediately adds "eco_friendly": EcoFriendlyShipping into _strategies.
Any client can now pass strategy_name="eco_friendly" to Order().
Zero changes were made to Order, ShippingStrategy, or ShippingStrategyRegistry!

Summary of Key Takeaways
----------------------------
GoalHow : Example 3 achieves it

Separation of Algorithms :Each shipping method (Standard, Freight, International) 
calculates cost/days independently.

Auto-Selection Enginerecommend_strategy():implements business logic to auto-pick the right 
algorithm based on data.

Dynamic Plug-and-PlayThe: @register decorator allows adding new strategies seamlessly 
(Open/Closed Principle).

Rich Context State: ShipmentDetails gives strategies all necessary parameters to compute 
complex business formulas.

'''