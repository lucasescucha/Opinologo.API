import time

from multiprocessing.pool import ThreadPool

POOL_PROCESSES = 5
ONE_MINUTE_IN_SECONDS = 60

class RequestsDispatcher:
    def __init__(self, requestFunction, rpmLimit) -> None:
        self.requestFunction = requestFunction
        self.rpmLimit = rpmLimit

    def dispatchRequests(self, arguments):
        result = []

        lArguments = arguments.copy()
        while len(lArguments) > 0:
            nArguments = min(len(lArguments), self.rpmLimit)
            sArguments = [lArguments.pop() for _ in range(nArguments)]

            with ThreadPool(POOL_PROCESSES) as pool:
                start_time = time.time()
                result.extend(pool.map(self.requestFunction, sArguments))

                pool.close()
                pool.join()

            deltaTime = ONE_MINUTE_IN_SECONDS - (time.time() - start_time)
            if deltaTime > 0:
                time.sleep(deltaTime)
        
        return result
