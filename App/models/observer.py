class Observer:
    """
    Observer mixin for objects that receive updates from a Subject.

    Classes that inherit this mixin must implement `update(message)`.
    """

    def update(self, message):
        """
        Receive an update from a Subject.
        
        Args:
            message: Notification payload.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement the update(message) method."
        )