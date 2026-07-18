import abc
import asyncio
from dataclasses import dataclass, field, asdict
from typing import List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status

# =====================================================================
# 1. THE STORAGE/MEMORY LAYER (Slotted Data Class)
# =====================================================================
@dataclass(slots=True)
class AbstractClusterNode(abc.ABC):
    """
    Abstract Base Data Class.
    Enforces ultra-low memory usage and fixed schemas across all compute nodes.
    """
    model: str
    _price: float

    @abc.abstractmethod
    async def process_payload_async(self, data: str) -> str:
        """Enforced asynchronous interface contract."""
        pass

@dataclass(slots=True)
class ComputeNode(AbstractClusterNode):
    """
    Memory-dense concrete execution node.
    Optimized for running non-blocking asynchronous operations inside threads.
    """
    zone: str
    active_connections: List[str] = field(default_factory=list)

    async def process_payload_async(self, data: str) -> str:
        """Simulates an asynchronous I/O bound network operation."""
        # Yield control back to the event loop to mimic database or network delay
        await asyncio.sleep(0.05)
        return f"Node [{self.model}] completely processed payload '{data}'
                 in  region {self.zone}."

# =====================================================================
# 2. THE VALIDATION & TRANSFORMATION LAYER (Pydantic Schema)
# =====================================================================
class NodeSchema(BaseModel):
    """
    The Input/Output Data API Contract.
    Handles automatic parsing, contract matching, and type conversion.
    """
    model: str = Field(..., min_length=3, examples=["Compute-X"])
    price: float = Field(..., gte=0, examples=[599.99])
    zone: str = Field(..., pattern=r"^[a-z]{2}-[a-z]+-\d+$", examples=["us-east-1"])
    active_connections: List[str] = Field(default_factory=list)

    # --- THE FACTORY PATTERNS ---
    @classmethod
    def from_domain(cls, domain_node: ComputeNode) -> "NodeSchema":
        """
        Factory Method: Transforms a slotted domain object into an API schema.
        Maps the private variable structure seamlessly to a clean public contract.
        """
        return cls(
            model=domain_node.model,
            price=domain_node._price,  # Safely translate private attributes 
     # to public fields
            zone=domain_node.zone,
            active_connections=domain_node.active_connections
        )

    def to_domain(self) -> ComputeNode:
        """
        Factory Method: Transforms an API schema back into a high-performance 
        domain instance.
        """
        return ComputeNode(
            model=self.model,
            _price=self.price,
            zone=self.zone,
            active_connections=self.active_connections
        )


# =====================================================================
# 3. THE PIPELINE ENGINE (FastAPI Asynchronous Routing REST API)
# =====================================================================
app = FastAPI(
    title="High-Performance Microservice Pipeline",
    description="Asynchronous processing framework combining slotted memory spaces with Pydantic contracts.",
    version="1.0.0"
)

# In-memory mock cloud database to store our slotted ComputeNode objects
NODE_DATABASE: dict[str, ComputeNode] = {}

@app.post(
    "/nodes", 
    response_model=NodeSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Register an optimized Compute Node"
)
async def register_node(payload: NodeSchema):
    """
    Receives incoming JSON data, transforms it automatically through 
    Pydantic constraints, maps it via a factory pattern into a 
    memory-optimized domain object, and saves it.
    """
    if payload.model in NODE_DATABASE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Node identification cluster '{payload.model}' already allocated."
        )
    
    # 1. Map validated input schema over to high-performance domain memory spaces
    domain_node = payload.to_domain()
    
    # 2. Persist the slotted instance within our cloud datastore map
    NODE_DATABASE[domain_node.model] = domain_node
    
    # 3. Use factory mapper to serialize the exact output back to standard 
    #     API JSON layout
    return NodeSchema.from_domain(domain_node)

@app.post(
    "/nodes/{model_id}/process", 
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger non-blocking execution payload calculations"
)
async def process_cluster_workload(model_id: str, payload_data: str):
    """
    Fetches the memory-dense slotted element directly out of the cluster dictionary 
    and handles computation asynchronously without locking down the system threadpool loop.
    """
    # Look up the high-performance object instance
    node = NODE_DATABASE.get(model_id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Target compute hardware node '{model_id}' was not located."
        )
    
    # Run the abstract implementation asynchronously 
    execution_result = await node.process_payload_async(payload_data)
    
    return {"status": "success", "execution_logs": execution_result}


# =====================================================================
# LOCAL SIMULATION PLATFORM RUNTIME
# =====================================================================
if __name__ == "__main__":
    import uvicorn
    print("\n[Bootloader] Running integration checks on our factory mapping matrix...")
    # Local verification loop to validate components outside of 
    # active server lifecycles
    test_schema = NodeSchema(model="Alpha-Unit", 
price=1200.0, 
zone="eu-west-1", 
active_connections=["10.0.0.5"]
    )
    
    # Test conversion: Schema -> Slotted Object
    slotted_obj = test_schema.to_domain()
    assert hasattr(slotted_obj, "__slots__"), "Failure: Factory instance is unoptimized!"
    
    # Test conversion: Slotted Object -> Schema
    rebuilt_schema = NodeSchema.from_domain(slotted_obj)
    assert rebuilt_schema.price == 1200.0, "Failure: Data corruption detected in mapping pipeline."
    print("[Bootloader] System integrity checks passed successfully.")
    print("[Bootloader] Launching Uvicorn Asynchronous Service Layer on port 8000...\n")
    # Launch local development server loop
    uvicorn.run(app, host="127.0.0.1", port=8000)
