class DashboardController:
    def __init__(self, view, container):
        self.view = view
        self.service = container.dashboard_service