
from screeninfo import get_monitors

def get_display_resolution(display_index: int) -> tuple[int, int] | None:
    """
    
        Returns the Resolution of the Display.

        Args:
            display_index (int): The Index of the Display. (0 = Main Display)

        Returns:
            tuple[int, int] | None: X, Y or None, if the Display information cannot be gathered or doesn't exist.
    
    """
    
    if display_index < 0:
        # TODO: Connect to Failure System
        return None

    displays = get_monitors()
    if display_index >= len(displays):
        # TODO: Connect to Failure System
        return None
    
    target_display = displays[display_index]
    return (target_display.width, target_display.height)
