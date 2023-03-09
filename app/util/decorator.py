import time
from functools import wraps
from app.util.logger import logger


def validated_parameters(zip_method):
    """ Validate parameters of ParameterZipper.zip """
    @wraps(zip_method)
    def wrapped(*args, **kwargs):
        for arg in args[1:]:
            if not isinstance(arg, (list, type(None))):
                logger.error(f"{arg} type error - must be 'list or none type' but '{type(arg)}'")
                raise TypeError("The parameters must be list or none type")

        for kwarg in kwargs.values():
            if not isinstance(kwarg, (list, type(None))):
                logger.error(f"{kwarg} type error - must be 'list or none type' but '{type(kwarg)}'")
                raise TypeError("The parameters must be list or none type")

        return zip_method(*args, **kwargs)
    return wrapped


def trace_function_execution_time(attr_name: str = ""):
    """ Trace execution time of the function """
    def wrapped1(function):
        @wraps(function)
        def wrapped2(*args, **kwargs):
            self_: object = args[0]

            attr = ""
            if attr_name:
                try:
                    attr = self_.__getattribute__(attr_name)
                except AttributeError:
                    pass
            obj = attr or self_.__class__.__name__

            start_time = time.time()
            execution = function(*args, **kwargs)
            end_time = time.time()
            logger.info(f"{obj} {function.__name__}() - {end_time - start_time:.3f}s.")
            return execution
        return wrapped2
    return wrapped1


def trace_async_function_execution_time(function):
    """ Trace execution time of the async function """
    @wraps(function)
    async def wrapped(*args, **kwargs):
        start_time = time.time()
        execution = await function(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Execution time of {function.__name__}() - {end_time - start_time:.3f}s.")
        return execution
    return wrapped


def repeat_until_no_exception(chances: int = 1, waiting: float = 2.0, exceptions=None):
    """ Repeat the function until no exception occurs """
    if exceptions is None:
        exceptions = [RuntimeError]

    def wrapped1(function):
        @wraps(function)
        def wrapped2(*args, **kwargs):
            for chance in range(chances, 0, -1):
                try:
                    return function(*args, **kwargs)
                except tuple(exceptions):
                    logger.debug(f"{function.__name__} will be repeat after {waiting} second.")
                    time.sleep(waiting)
            logger.debug(f"{function.__name__}(args:{args}, kwargs:{kwargs}) cannot execute.")
        return wrapped2
    return wrapped1
