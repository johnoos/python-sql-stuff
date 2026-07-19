import json
import abc

# =====================================================================
# 1. THE METACLASS (Dynamic Validation Framework)
# =====================================================================
class SystemValidationMeta(type):
    """
    A Custom Metaclass.
    
    Intercepts class creation to enforce documentation rules across the system.
    """
    def __new__(mcs, name, bases, namespace):
        if name != "AbstractSmartDevice" and not namespace.get("__doc__"):
            raise TypeError(f"Architecture Violation: Class '{name}' must have a docstring!")
        return super().__new__(mcs, name, bases, namespace)


# =====================================================================
# 2. THE ABSTRACT BASE CLASS (API Contract Enforcement)
# =====================================================================
class AbstractSmartDevice(metaclass=SystemValidationMeta):
    """
    An Abstract Base Class (ABC) driven by our custom Metaclass.
    
    Defines the structural blueprint for child objects.
    """
    
    # Define slots at the abstract layer so memory savings cascade downwards
    __slots__ = ("model", "_price")

    def __init__(self, model: str, price: float):
        self.model = model
        self._price = price

    @abc.abstractmethod
    def process_core_payload(self) -> str:
        pass


# =====================================================================
# 3. THE OPTIMIZED PRODUCTION CLASS WITH __slots__
# =====================================================================
class HighPerformanceNode(AbstractSmartDevice):
    """
    A low-latency system node optimized for massive memory reductions 
    and fast variable read/write speeds using __slots__.
    """
    
    # OPTIMIZATION HOOK: Tells Python to allocate memory for exactly 
    # these attributes, instead of creating a heavy __dict__ hash map for every object.
    __slots__ = ("zone", "_active_connections")

    def __init__(self, model: str, price: float, zone: str):
        # Trigger parent constructor architecture
        super().__init__(model, price)
        self.zone = zone
        self._active_connections = []

    def process_core_payload(self) -> str:
        return f"Node [{self.model}] processed payload in zone {self.zone}."

    @property
    def price(self) -> float:
        return self._price


# =====================================================================
# 4. CUSTOM JSON ENCODER (Serializing __slots__ classes)
# =====================================================================
class DeviceJsonEncoder(json.JSONEncoder):
    """
    A Custom JSON Encoder.
    
    Standard Python objects are converted to JSON by reading their internal '__dict__'.
    Because classes using '__slots__' do not have a '__dict__', this custom encoder 
    manually gathers properties and slot values to serialize them cleanly.
    """
    def default(self, obj):
        if isinstance(obj, AbstractSmartDevice):
            # Gather all slotted attribute names across the inheritance chain
            all_slots = set()
            for cls in obj.__class__.__mro__:
                slots = getattr(cls, "__slots__", None)
                if slots:
                    # Handle single string slots or tuple/list slots safely
                    if isinstance(slots, str):
                        all_slots.add(slots)
                    else:
                        all_slots.update(slots)

            # Build a safe data dictionary of attributes we want to serialize
            serialized_data = {}
            for slot in all_slots:
                # Bypass raw underscores for cleaner public key mappings in JSON
                clean_key = slot.lstrip("_") 
                serialized_data[clean_key] = getattr(obj, slot)
                
            return serialized_data
            
        # Fallback to standard encoder behavior for primitives (strings, lists, etc.)
        return super().default(obj)


# =====================================================================
# DEMONSTRATION ENGINE
# =====================================================================
if __name__ == "__main__":
    print("--- 1. Verification of __slots__ Memory Optimization ---")
    node = HighPerformanceNode("Edge-Computing-Unit", 450.00, "us-west-1")

    # Accessing attributes works perfectly like standard classes
    print(f"Node Model: {node.model}")
    print(f"Node Price: ${node.price}")

    # VERIFICATION: Confirming __dict__ does not exist on this object
    try:
        print(node.__dict__)
    except AttributeError:
        print("Success: node.__dict__ does not exist! Memory optimization is active.")

    # LOCKDOWN TEST: Trying to add an undeclared attribute on the fly will crash
    try:
        node.unregistered_variable = "Dynamic Hack Attempt"
    except AttributeError as e:
        print(f"Success: Dynamically appending variables was blocked. Reason: {e}")


    print("\n--- 2. Custom JSON Serialization ---")
    node._active_connections.extend(["10.0.0.4", "192.168.1.1"])

    # Pass our custom encoder into json.dumps() to process the slotted object
    json_output = json.dumps(node, cls=DeviceJsonEncoder, indent=4)
    print("Generated JSON Output String:")
    print(json_output)
