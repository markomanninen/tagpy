from IPython.core.magic import register_line_magic
from IPython.display import HTML
from tagpy import helper as h, table

@register_line_magic
def runtests(line):
    """
    The %runtests magic searches your IPython namespace for functions
    with names that begin with 'test'. It will attempt to run these
    functions (calling them with no arguments), and report whether they
    pass, fail (raise an AssertionError), or error (raise any other
    kind of error).

    For tests that fail or error %runtests will show the exception raised
    but not the traceback, so write informative messages!

    """
    import collections
    import time

    ip = get_ipython()

    tests = {}

    # collect tests
    # search will only find functions that start with 'test'
    for k, v in ip.user_ns.iteritems():
        if k.startswith('test') and isinstance(v, collections.Callable):
            tests[k] = v

    tbl = table(CLASS='data')
    tbl.addColGroup(h.col(), h.col())
    tbl.addCaption('Collected {} tests.\n'.format(len(tests)))
    tbl.addHeadRow(h.tr(h.th('Test function name'), h.th('Status')))

    # run tests
    ok = 0
    fail = {}
    error = {}

    t1 = time.time()

    for name, func in tests.iteritems():
        try:
            func()
        except AssertionError as e:
            msg = 'failed'
            fail[name] = e
        except Exception as e:
            msg = 'error'
            error[name] = e
        else:
            msg = 'successful'
            ok += 1
        tbl.addBodyRow(h.tr(h.td(name), h.td(msg), Class=msg))

    t2 = time.time()

    # print info on any failures
    if fail:
        tbl.addBodyRows(h.tr(h.th("Failed", span=2)))
        trs = []
        for name, e in fail.iteritems():
            trs.append(h.tr(h.td(name), h.td(repr(e))))
        tbl.addBodyRows(*trs, CLASS='failures')

    # print info on any errors
    if error:
        tbl.addBodyRows(h.tr(h.th("Errors", span=2)))
        trs = []
        for name, e in error.iteritems():
            trs.append(h.tr(h.td(name), h.td(repr(e))))
        tbl.addBodyRows(*trs, CLASS='errors')

    # summary and timer of the tests
    tbl.addFootRow(h.tr(h.td('Successful', Class="right"), h.td('{}'.format(ok))))
    tbl.addFootRow(h.tr(h.td('Failed',     Class="right"), h.td('{}'.format(len(fail)))))
    tbl.addFootRow(h.tr(h.td('Errors',     Class="right"), h.td('{}'.format(len(error)))))
    tbl.addFootRow(h.tr(h.td("Excecution", Class="right"), h.td('{:.3g} seconds'.format(t2 - t1))))
    return HTML(str(tbl))