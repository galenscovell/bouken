class IMapGenerator:
    """
    Interface for procedurally generating maps.
    """
    def instantiate(self, *args) -> None:
        """Setup initial params for new map to be generated."""
        pass

    def generate(self) -> str:
        """Actually generate the most recently instantiated map."""
        pass

    def serialize(self) -> str:
        """Serialize generated map to JSON string."""
        pass
