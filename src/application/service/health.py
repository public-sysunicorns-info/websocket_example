

class HealthService:

    liveness: bool
    readiness: bool
    health: bool

    cache_health: bool

    def __init__(self):
        #
        self.liveness = False
        self.readiness = False
        self.health = False
        #
        self.cache_health = False

    def set_cache_health(self, cache_health: bool) -> None:
        self.cache_health = cache_health
        self._calculate()

    def get_health(self) -> bool:
        return self.health

    def _calculate(self) -> None:
        if self.cache_health:
            self.liveness = True
            self.readiness = True
            self.health = True
        else:
            self.liveness = False
            self.readiness = False
            self.health = False
