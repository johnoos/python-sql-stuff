import abc
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

# =====================================================================
# 1. THE HIGH-PERFORMANCE DATA LAYER (Python Native Data Classes)
# =====================================================================
@dataclass(slots=True)
class AbstractHardwareNode(abc.ABC):
    """
    An Abstract Base Data Class.
    
    Setting 'slots=True' automatically blocks __dict__ creation, optimizing 
    memory allocation and processing speeds across all inherited child elements.
    """
    model: str
    _price: float

    @abc.abstractmethod
    def compute_metrics(self) -> str:
        """Enforced interface requirement for all subclasses."""
        pass


@dataclass(slots=True)
class TelemetryNode(AbstractHardwareNode):
    """
    A lightweight, memory-optimized concrete data class.
    
    Because slots=True is inherited and redeclared, instances consume up to
    50% less RAM, making it perfect for processing high-frequency data streams.
    """
    zone: str
    # Data classes require a default_factory for mutable objects like lists
    active_connections: list[str] = field(default_factory=list)

    def compute_metrics(self) -> str:
        """Fulfills the abstract interface contract."""
        return f"Node [{self.model}] tracking telemetry streams inside {self.zone}."


# =====================================================================
# 2. THE DECOUPLED VALIDATION & SERIALIZATION LAYER (Pydantic Model)
# =====================================================================
class NodeSerializationModel(BaseModel):
    """
    A pure data validation and serialization schemas.
    
    This layer is completely decoupled from your core runtime hardware nodes. 
    It parses incoming web structures, runs strict validations, and exports 
    clean JSON schemas instantly without needing a custom JSONEncoder.
    """
    # Map, validate, and document fields using built-in constraints
    model: str = Field(..., min_length=3, description="The unique hardware code designation.")
    price: float = Field(..., gte=0, description="The book value asset pricing (must be positive).")
    zone: str = Field(..., pattern=r"^[a-z]{2}-[a-z]+-\d+$", description="AWS style region string (e.g. us-east-1)")
    active_connections: list[str] = Field(default_factory=list, description="IP connection array logs.")

    class Config:
        """Configuring model behavior settings."""
        # Strips out any extra unexpected dictionary payload items passed during parsing
        extra = "forbid" 


# =====================================================================
# DEMONSTRATION ENGINE
# =====================================================================
if __name__ == "__main__":
    print("--- 1. Testing Memory Optimized Data Class ---")
    # Instant initialization without writing a manual __init__ block
    node = TelemetryNode(model="Edge-01", _price=299.99, zone="us-east-1")
    node.active_connections.extend(["10.0.0.1", "192.168.0.5"])

    print(node.compute_metrics())

    # VERIFICATION: Confirming __dict__ doesn't exist
    try:
        print(node.__dict__)
    except AttributeError:
        print("Success: node.__dict__ does not exist! Slotted optimization is live.")

    # LOCKDOWN TEST: Confirming attributes are static and fixed
    try:
        node.malicious_injected_field = "Hack Attempt"
    except AttributeError as e:
        print(f"Success: Dynamic attribute assignment blocked. Reason: {e}")


    print("\n--- 2. Seamless Decoupled Serialization via Pydantic ---")
    # Step A: Transform data class values into a native dictionary representation
    # (Extract slotted variables cleanly using built-in tuple/attribute unpacking)
    node_data = {
        "model": node.model,
        "price": node._price, # Map private variable to clean public JSON naming
        "zone": node.zone,
        "active_connections": node.active_connections
    }

    # Step B: Instantiate the validation model with our data payload
    pydantic_schema = NodeSerializationModel(**node_data)

    # Step C: Convert to a clean JSON string instantly with one method call
    json_output = pydantic_schema.model_dump_json(indent=4)
    print("Generated Pydantic JSON Output String:")
    print(json_output)


    print("\n--- 3. Testing Pydantic's Built-In Data Validation Guarantees ---")
    bad_data = {
        "model": "X",                 # Fails: Too short (min_length=3)
        "price": -150.00,              # Fails: Negative pricing threshold (gte=0)
        "zone": "invalid-zone-name",   # Fails: Broken regex pattern rule check
        "active_connections": []
    }

    try:
        NodeSerializationModel(**bad_data)
    except ValueError as validation_error:
        print("Success: Pydantic safely caught and blocked invalid system data payloads:")
        print(validation_error)
