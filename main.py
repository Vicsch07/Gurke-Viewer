


def main():
    print("=== INITIALIZING GURKE VIEWER ===")
    
    from states import state_manager

    state_manager.reset_ui_state_file("ui_state")

    from ui import main_window

if __name__ == "__main__":
    main()
