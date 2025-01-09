class AgentNotFound(Exception):
    def __init__(self):
        super(AgentNotFound, self).__init__("Agent doesn't exists.")
