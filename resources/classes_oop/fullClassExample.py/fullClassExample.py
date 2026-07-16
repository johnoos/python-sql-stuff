class SmartDevice:
    """
    An extended Python class demonstrating properties (@property), 
    mathematical dunder methods, container protocol dunder methods,
    weak private methods, and strong private methods (Name Mangling).
    """

    device_count = 0

    def __init__(self, model: str, price: float, storage_gb: int):
        self.model = model
        self._price = price          # Private attribute managed by properties
        self._storage_gb = storage_gb
        # Private internal list for container dunder methods
        self._installed_apps = []     
        
        SmartDevice.device_count += 1

    # =====================================================================
    # 1. PROPERTIES (Controlled access to private attributes)
    # =====================================================================
    @property
    def price(self) -> float:
        """
        The Getter Property.
        
        This intercepts access to the private self._price attribute.
        It allows external users to read the data using 'device.price' 
        without trailing parentheses, making it look like a standard attribute.
        """
        return self._price

    @price.setter
    def price(self, new_price: float):
        """
        The Setter Property.
        
        This intercepts assignment statements like 'device.price = 500'.
        It acts as a gatekeeper, allowing you to validate data or run
        checks before modifying the actual underlying private self._price variable.
        """
        if new_price < 0:
            raise ValueError("Price cannot be negative!")
        self._price = new_price

    @property
    def storage_gb(self) -> int:
        """
        Read-Only Property.
        
        By omitting a corresponding @storage_gb.setter method, this attribute 
        becomes read-only. External code can view the storage value but 
        cannot alter it, enforcing immutability after object creation.
        """
        return self._storage_gb


    # =====================================================================
    # 2. MATHEMATICAL DUNDERS (Operator Overloading)
    # =====================================================================
    def __add__(self, other) -> float:
        """
        The 'Addition' Dunder Method.
        
        Syntax Trigger: triggered automatically by the '+' operator (e.g., object1 + object2).
        
        This method defines what happens when this object is on the LEFT side of the plus sign.
        It checks if the other object is another SmartDevice or a raw number, 
        and adds their values together accordingly.
        """
        if isinstance(other, SmartDevice):
            return self.price + other.price
        elif isinstance(other, (int, float)):
            return self.price + other
        return NotImplemented

    def __radd__(self, other) -> float:
        """
        The 'Right-Side Addition' Dunder Method.
        
        Syntax Trigger: triggered by the '+' operator when this object is on the RIGHT side 
        of the plus sign, and the left object doesn't know how to handle it (e.g., number + object).
        
        This acts as a fallback. It reroutes the operation back to our main __add__ method 
        to ensure math operations work seamlessly regardless of operand order.
        """
        return self.__add__(other)


    # =====================================================================
    # 3. CONTAINER DUNDERS (Making objects behave like lists/dicts)
    # =====================================================================
    def __len__(self) -> int:
        """
        The 'Length' Dunder Method.
        
        Syntax Trigger: triggered automatically when passing the object to the built-in len() function.
        
        Instead of forcing users to look up an internal list, this allows them to query 
        the device directly to see how many items (apps) it contains internally.
        """
        return len(self._installed_apps)

    def __getitem__(self, index: int) -> str:
        """
        The 'Get Item' Dunder Method.
        
        Syntax Trigger: triggered by bracket notation for reading data (e.g., device[index]).
        
        This maps square-bracket lookups directly onto our private internal list, 
        making the instance object itself behave transparently like a sequence or collection.
        """
        return self._installed_apps[index]

    def __setitem__(self, index: int, app_name: str):
        """
        The 'Set Item' Dunder Method.
        
        Syntax Trigger: triggered by bracket notation for changing data (e.g., device[index] = value).
        
        This intercepts element assignment via square brackets, allowing you to update 
        values inside the internal container safely.
        """
        self._installed_apps[index] = app_name


    # =====================================================================
    # 4. PRIVATE METHODS & NAME MANGLING
    # =====================================================================
    def boot_device(self):
        """Public API method used to turn on the machine."""
        print(f"Booting up {self.model}...")
        
        # 1. Calling the weak private method internally
        self._check_battery()
        
        # 2. Calling the strong private method internally
        self.__load_firmware()

    def _check_battery(self):
        """
        Weak Private Method (Single Underscore).
        
        Syntax Mechanism: Purely a naming convention. Python does NOT restrict access 
        to this method from the outside. 
        
        It acts as a gentle warning to other developers that this is an internal 
        helper method and should not be relied upon as a part of the public API.
        """
        print("Checking battery optimization status...")

    def __load_firmware(self):
        """
        Strong Private Method (Double Underscore / Name Mangling).
        
        Syntax Mechanism: Because of the double leading underscore, Python rewrites 
        the internal name of this method to '_SmartDevice__load_firmware'.
        
        This actively hides the method from external accidental calls and protects it from 
        being overridden by a child subclass.
        """
        print("Loading secure operating system layers...")


    # Helper method to add data to container
    def install_app(self, app_name: str):
        self._installed_apps.append(app_name)


# =====================================================================
# DEMONSTRATION
# =====================================================================
if __name__ == "__main__":
    device1 = SmartDevice("Nexus X", 600.00, 128)
    device2 = SmartDevice("Echo Lite", 200.00, 64)

    print("--- 1. Testing Properties ---")
    print(f"Device 1 Price: ${device1.price}")
    device1.price = 550.00
    print(f"New Device 1 Price: ${device1.price}")
    
    try:
        device1.price = -50.00
    except ValueError as e:
        print(f"Caught expected error: {e}")


    print("\n--- 2. Testing Math Overloading ---")
    total_cost = device1 + device2
    print(f"Combined package cost: ${total_cost}")


    print("\n--- 3. Testing Container Magic Methods ---")
    device1.install_app("Spotify")
    device1.install_app("Netflix")
    print(f"Total apps installed: {len(device1)}")
    print(f"Primary app: {device1}")


    print("\n--- 4. Testing Method Privacy Levels ---")
    # Calling the public method works perfectly and executes both private methods internally
    device1.boot_device()

    print("\nExternal access checks:")
    
    # WEAK PRIVATE ACCESS: Works fine because it is just a naming convention
    device1._check_battery() 

    # STRONG PRIVATE ACCESS: Will CRASH with an AttributeError!
    try:
        device1.__load_firmware()
    except AttributeError:
        print("Caught expected AttributeError: Direct external access to '__load_firmware' was blocked!")

    # Bypassing Strong Privacy intentionally via Python's underlying syntax mapping:
    print("\nBypassing strong protection manually:")
    device1._SmartDevice__load_firmware() # Output: Loading secure operating system layers...
