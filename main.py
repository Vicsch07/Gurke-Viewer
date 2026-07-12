def main():
    print("=== INITIALIZING GURKE VIEWER ===")

    from states import state_manager
    import sys

    # Reset states before starting up modules
    state_manager.reset_ui_state_file("ui_state")

    
    from ui import main_window
    print("=== EXITING GURKE VIEWER ===")
    sys.exit()

if __name__ == "__main__":
    main()
