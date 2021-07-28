def partial(func : Callable, *args, **kwargs):
    '''
        partial
        Simple implementation for false currying
        :: func     :: Function to curry
        :: *args    :: Positional arguments
        :: **kwargs :: Keyword arguments
    '''
    def p_func(*p_args, **p_kwargs):
        return func(*args, *p_args, **kwargs, **p_kwargs)
    return p_func
