class CommandHandler:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def handle(self, command):
        if command == "/clean_now":
            return self.orchestrator.run_pipeline()
        return "Unknown command."
