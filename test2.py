import threadpool


def hello(m, n, o1):
    """"""
    print( "m = %s, n = %s, o = %s" % (m, n, o1))


if __name__ == '__main__':
    # 方法1
    # lst_vars_1 = ['1', '2', '3']
    # lst_vars_2 = ['4', '5', '6']
    # func_var = [(lst_vars_1, None), (lst_vars_2, None)]
    # 方法2
    dict_vars_1 = {'m': '1', 'n': '2', 'o': '3'}
    dict_vars_2 = {'m': '4', 'n': '5', 'o': '6'}
    func_var = [(None, dict_vars_1), (None, dict_vars_2)]

    pool = threadpool.ThreadPool(2)
    requests = threadpool.makeRequests(hello, func_var)
    [pool.putRequest(req) for req in requests]
    pool.wait()