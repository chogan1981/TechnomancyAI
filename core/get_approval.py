def get_approval(prompt_text):
    """
    Prompts the user for y/n confirmation. Returns True if 'y', False if 'n'.
    Keeps prompting until a valid input is received.
    """
    while True:
        user_input = input(f"{prompt_text} [y/n]: ").strip().lower()
        if user_input in ('y', 'n'):
            return user_input == 'y'
        print("Please enter 'y' or 'n'.")