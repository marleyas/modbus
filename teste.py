from time import sleep
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from rich import print
from rich.live import Live
from rich.table import Table
import keyboard
import os 

client_modbus = ModbusClient(
    method='rtu', 
    port='COM3', 
    stopbits=1, 
    parity='N', 
    baudrate=9600
)

# endereço do dispositivo
addr = 0xC8

def read_input_output():
    _read = client_modbus.read_input_registers(0xFA65, 0x0003, unit=addr)

    _io = []
    _regs = []
    if not _read.isError():
        _regs = _read.registers
        print(_regs)
        for index, value in enumerate([1, 2, 4, 8, 16, 32, 64 ,128]):
            _obj = ('DI' + str(index), bool(_regs[1] & value))
            _io.append(_obj)
        _obj = ('AI0', _regs[2])        
        _io.append(_obj)
        for index, value in enumerate([1, 2]):
            _obj = ('DO' + str(index), bool(_regs[2] & value))
            _io.append(_obj)        
    return _io, _regs

def high_output(_io):
    _, _regs = read_input_output()
    if _io == "DO0":
        _new_val = _regs[2] | 1
    else:
        _new_val = _regs[2] | 2
    #print("[green]Liga " + _io + " " + str(_new_val))
    _write = client_modbus.write_register(0xFBF4, _new_val, unit=addr)
    
def low_output(_io):
    _, _regs = read_input_output()
    if _io == "DO0":
        _new_val = _regs[2] & 254
    else:
        _new_val = _regs[2] & 253
    #print("[red]Desliga " + _io + " " + str(_new_val))    
    _write = client_modbus.write_register(0xFBF4, _new_val, unit=addr)    
    
def generate_table():
    table = Table()
    table.add_column("I/O")
    table.add_column("Valor")
    _ios, _regs = read_input_output()        
    for item in _ios:
        if not item[1]:
            table.add_row(item[0], "[red]" + str(item[1]))
        else:
            table.add_row(item[0], "[green]" + str(item[1]))         
    return table
 
if __name__ == '__main__':
    print("[yellow]#======================================================#")
    print("[yellow]# Monitor de I/O'S do Datalogger da ABS Telemetria.    #")
    print("[yellow]# Para acionar a saída digital [blue]DO0 [yellow]use as teclas A e S.#")
    print("[yellow]# Para acionar a saída digital [blue]DO1 [yellow]use as teclas Z e X.#")
    print("[yellow]# Para encerrar a execução use a tecla Q.              #")
    print("[yellow]#======================================================#")
    with Live(generate_table(), refresh_per_second=4) as live:
        keyboard.on_press_key("q", lambda _:os._exit(os.X_OK))
        keyboard.on_press_key("a", lambda _:high_output("DO0"))
        keyboard.on_press_key("s", lambda _:low_output("DO0"))
        keyboard.on_press_key("z", lambda _:high_output("DO1"))
        keyboard.on_press_key("x", lambda _:low_output("DO1"))
        while True:
            sleep(1.0)
            live.update(generate_table())            