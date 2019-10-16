import os.path
try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

from opcua import ua, uamethod, Server
import time

from opcua import ua, Server
from random import randint
import datetime



@uamethod
def start_program(parent, program_01):
    if program_01:
        start = True
        # LED Grün leuchtet
        time.sleep(20)
        start = False
        beendet = True
        # LED Gelb leuchtet

    else:

        stoerung = True





@uamethod
def say_hello(parent, happy):
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(result)
    return result



@uamethod
def say_hello_xml(parent, happy, hugo):
    print("Calling say_hello_xml")
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(hugo)
    print(result)
    return result


@uamethod
def say_hello(parent, happy):
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(result)
    return result


@uamethod
def say_hello_array(parent, happy):
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(result)
    return [result, "Actually I am"]

@uamethod
def say_hello_hugo(parent):
    print('ich säge nüüt')
    return 'hugo'


class HelloServer:
    def __init__(self, endpoint, name, model_filepath):
        self.server = Server()


        #  This need to be imported at the start or else it will overwrite the data
        self.server.import_xml(model_filepath)

        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)

        objects = self.server.get_objects_node()

        freeopcua_namespace = self.server.get_namespace_index("urn:freeopcua:python:server")
        hellower = objects.get_child("0:Hellower")
        hellower_say_hello = hellower.get_child("0:SayHello")

        self.server.link_method(hellower_say_hello, say_hello_xml)

        hellower.add_method(
            freeopcua_namespace, "SayHello2", say_hello, [ua.VariantType.Boolean], [ua.VariantType.String], [ua.VariantType.String])

        hellower.add_method(
            freeopcua_namespace, "SayHelloArray", say_hello_array, [ua.VariantType.Boolean], [ua.VariantType.String])

        hellower.add_method(
            freeopcua_namespace, "SayHelloHugo", say_hello_hugo)

        hellower.add_method(
            freeopcua_namespace, "StartProgram", start_program, [ua.VariantType.Boolean], [ua.VariantType.String], [ua.VariantType.String])


        # add Parameter to the Object


        start = hellower.add_variable(0, "Temperature", False)
        stoerung = hellower.add_variable(0, "Stoerung", False)
        beendet = hellower.add_variable(0, "Beendet", False)

        Temp = hellower.add_variable(0, "Temperature", 0)
        Press = hellower.add_variable(0, "Pressure", 0)
        Time = hellower.add_variable(0, "Time", 0)

        Temp.set_writable()
        Press.set_writable()
        Time.set_writable()


        count = 0
        while True:
            time.sleep(5)
            Temperature = randint(10, 20)
            Pressure = randint(10, 20)
            TIME = datetime.datetime.now()

            print(Temperature, Pressure, TIME)
            Temp.set_value(Temperature)
            Press.set_value(Pressure)
            Time.set_value(TIME)

            time.sleep(5)


    def __enter__(self):
        self.server.start()
        return self.server

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.stop()


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    with HelloServer(
            "opc.tcp://0.0.0.0:40840/freeopcua/server/",
            "FreeOpcUa Example Server",
            os.path.join(script_dir, "test_saying.xml")) as server:

        embed()
