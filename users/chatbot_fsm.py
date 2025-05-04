class ChatFSM:
    # Define all valid chatbot states in order
    states = ["start", "age", "user_type", "income", "rental_income", "section_80C", "summary"]

    def __init__(self, session):
        self.session = session
        # Initialize chatbot state if not present
        if "chat_state" not in self.session:
            self.session["chat_state"] = self.states[0]
            self.session.modified = True

    def next_state(self):
        """Move to the next chatbot state.
           If the current state is invalid, reset to the first state."""
        current_state = self.session.get("chat_state", self.states[0])
        try:
            index = self.states.index(current_state)
        except ValueError:
            # Reset to start if the current state is unrecognized.
            index = 0
            self.session["chat_state"] = self.states[0]
            self.session.modified = True

        if index + 1 < len(self.states):
            self.session["chat_state"] = self.states[index + 1]
            self.session.modified = True
        return self.session["chat_state"]

    
    def reset(self):
        """Reset the chatbot to the initial state."""
        self.session["chat_state"] = self.states[0]
        self.session.modified = True

        # Inside ChatFSM class
    def get_state(self):
        state = self.session.get("chat_state", "greeting")
        print(f"Current state: {state}")  # Debug print
        return state

    def set_state(self, new_state):
        print(f"Setting state to: {new_state}")  # Debug print
        self.session["chat_state"] = new_state
        self.session.modified = True
