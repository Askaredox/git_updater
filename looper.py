import time


class Looper:
    __lastTime = 0

    def __init__(self, delay) -> None:
        self.DELAY = delay
        self.init()
        self.__loop()

    def init(self) -> None:
        raise NotImplementedError("Implement the init method on Looper class")

    def get_time(self):
        return self.DELAY[0] * 1000 +\
            self.DELAY[1] * (60 * 1000) +\
            self.DELAY[2] * (60 * 60 * 1000) +\
            self.DELAY[3] * (24 * 60 * 60 * 1000)

    def millis(self):
        return round(time.time() * 1000)

    def loop(self) -> None:
        raise NotImplementedError("Implement the loop method on Looper class")

    def __loop(self) -> None:
        try:
            while(1):
                if((self.millis() - self.__lastTime) >= self.get_time()):
                    self.__lastTime = self.millis()
                    self.loop()
        except KeyboardInterrupt:
            print('Stoping loop!')
        except Exception as ex:
            print(ex)

