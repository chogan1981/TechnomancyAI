from error_handling import handle_exception, log_with_context

def error_handling_decorator(context, re_raise=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_with_context(e, context)
                handle_exception(e)
                if re_raise:
                    raise
                return None
        return wrapper
    return decorator