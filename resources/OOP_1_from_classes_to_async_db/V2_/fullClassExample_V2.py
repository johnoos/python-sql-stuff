class SmartDevice:
    """
    An advanced, production-grade Python class demonstrating:
    - Custom Context Managers (__enter__ and __exit__)
    - Callable Instances (__call__)
    - Method inheritance properties with privacy levels
    """
    device_count = 0

    def __init__(self, model: str, price: float, storage_gb: int):
        self.model = model
        self._price = price          
        self._storage_gb = storage_gb
        self._installed_apps = []     
        self.is_connected = False  # Track state for the context manager
        
        SmartDevice.device_count += 1

    # =====================================================================
    # 1. CALLABLE INSTANCES (Making objects behave like functions)
    # =====================================================================
    def __call__(self, task_name: str) -> str:
        """
        The 'Call' Dunder Method.
        
        Syntax Trigger: triggered automatically by using parentheses 
        on an instance variable.
        Example: device_instance("Run Diagnostic")
        
        This allows an object to behave like a standard reusable function, 
        maintaining internal state between execution calls.
        """
        print(f"[Execution Layer] Processing task sequence...")
        return f"Task '{task_name}' completed successfully on {self.model}."


    # =====================================================================
    # 2. CONTEXT MANAGERS (Resource Allocation Control via 'with' statements)
    # =====================================================================
    def __enter__(self):
        """
        The 'Enter' Dunder Method.
        
        Syntax Trigger: runs immediately when entering a 'with' block context.
        
        This method allocates resources, opens network tunnels, or connects 
        to external 
        hardware APIs. The value returned here is assigned to the variable 
        after 'as'.
        """
        print(f"\n[Context System] Connecting securely to {self.model} data stream...")
        self.is_connected = True
        return self  # Return self so it can be captured by the 'as' keyword

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        The 'Exit' Dunder Method.
        
        Syntax Trigger: runs automatically when exiting a 'with' block (even if an error 
        occurs).
        
        This method is critical for safe clean-up (closing ports, committing database 
        changes).
        If an exception happens inside the block, details are passed to exc_type, exc_val, 
        and exc_tb. 
        Returning True suppresses any raised exception. 
        Returning False allows it to bubble up.
        """
        print(f"[Context System] Disconnecting from {self.model} data stream safely.")
        self.is_connected = False
        
        if exc_type:
            print(f"[Context System] Handled an internal block exception safely: {exc_val}")
            return True  # Suppress the exception so the code outside doesn't crash
        return False     # No exceptions occurred


    # =====================================================================
    # 3. INTERNALS FOR INHERITANCE DEMONSTRATION
    # =====================================================================
    def run_diagnostics(self):
        """Public API method that invokes private helpers."""
        self._weak_internal_check()
        self.__strong_mangled_check()

    def _weak_internal_check(self):
        """Weak Private Method. Subclasses CAN access and override this directly."""
        print("Base Device: Performing standard system analysis...")

    def __strong_mangled_check(self):
        """Strong Private Method. Name-mangled. Subclasses CANNOT overwrite this."""
        print("Base Device: Executing core kernel security integrity test...")


# =====================================================================
# 4. INHERITANCE SUBCLASS (Demonstrating how privacy changes behavior)
# =====================================================================
class SuperComputer(SmartDevice):
    """A specialized subclass of SmartDevice to showcase method overriding rules."""
    
    def _weak_internal_check(self):
        """Successfully overrides the parent method completely."""
        print("SuperComputer: Performing advanced multi-threaded quantum system analysis!")

    def __strong_mangled_check(self):
        """
        This does NOT override SmartDevice's __strong_mangled_check.
        Because of name mangling, Python views this as an entirely independent method 
        named '_SuperComputer__strong_mangled_check'.
        """
        print("SuperComputer: Running subclass localized security routines...")


# =====================================================================
# DEMONSTRATION
# =====================================================================
if __name__ == "__main__":
    print("--- 1. Testing __call__ (Object as a Function) ---")
    server = SmartDevice("Mainframe X", 4500.00, 2048)
    
    # Triggering __call__ directly on the instance variable
    result = server("System Update Check")
    print(result)

    print("\n--- 2. Testing Context Manager Patterns ---")
    # Triggering __enter__ and __exit__ blocks automatically
    with server as connected_device:
        print(f"Device live connection status inside block: {connected_device.is_connected}")
        # Run standard operations inside the controlled block scope
        print(connected_device("Sync Databases"))
        
    print(f"Device live connection status outside block: {server.is_connected}")

    print("\n--- 3. Testing Context Manager Error Handling Safely ---")
    with server as connected_device:
        print("Forcing a deliberate ZeroDivisionError inside the with-block loop...")
        crash_trigger = 10 / 0  # This will fail
        print("This line will never execute.")

    print("The code continues executing smoothly because __exit__ intercepted the failure!")

    print("\n--- 4. Testing Inheritance & Privacy Scopes ---")
    quantum_node = SuperComputer("Quantum V1", 89000.00, 16384)
    
    # Executes the public inherited method from the parent class
    quantum_node.run_diagnostics()
