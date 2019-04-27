"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

import traceback


def directions():
    """ Returns a STRING body with the calculator directions """

    directions_body = """
    <h1>Welcome to the Calculator!<h1>
    
    <h2>You provide the function and the numbers in the URL and I do the rest.</h2>
    
    <h3>Type the following into your browser URL box:</h3>
    
    <h4>http://localhost:8080/add/2/3 to add 2 + 3</h4>
    <h4>http://localhost:8080/subtract/5/3 to subtract 3 from 5</h4>
    <h4>http://localhost:8080/multiply/5/2 to multiply 2 x 3</h4>
    <h4>http://localhost:8080/divide/10/5 to divide 10 by 2</h4>
    
    """

    return directions_body


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    sum_result = sum(map(int, args))

    return str(sum_result)


def subtract(*args):
    """ Returns a STRING body with the arguments subtracted """

    sub_result = int(args[0]) - int(args[1])

    return str(sub_result)


def multiply(*args):
    """ Returns a STRING body with the arguments multiplied """

    mul_result = int(args[0]) * int(args[1])

    return str(mul_result)


def divide(*args):
    """ Returns a STRING body with the arguments divided """

    div_result = int(args[0]) / int(args[1])

    return str(div_result)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '': directions,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):

    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "500 Internal Server Error"
        body = "<hl>Division by zero is not allowed!</hl>"
    except ValueError:
        status = "500 Internal Server Error"
        body = "<hl>Only numbers are allowed!</hl>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
