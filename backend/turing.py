import json
import time
import matplotlib.pyplot as plt


class TuringMachine:
    symbols: list[str]
    states: list[str]
    initial_state: str
    final_states: list[str]
    blank_symbol: str
    transitions: dict[str, dict[str, tuple[str, str, str]]]
    tape: list[str]

    def __init__(self, symbols, states, initial_state, final_states, blank_symbol, transitions, tape=None):
        self.symbols = symbols  # Alfabeto
        self.states = states  # Estados
        self.initial_state = initial_state  # Estado inicial
        self.final_states = final_states  # Estados finales
        self.blank_symbol = blank_symbol  # Símbolo blanco
        self.transitions = transitions  # Transiciones
        self.tape = tape  # Cinta

    def reset_tape(self, input_string: str) -> None:
        """Reinicia la cinta con la cadena de entrada y el símbolo en blanco"""
        self.tape = list(input_string)
        self.tape.append(self.blank_symbol)

    def simulate(self, input_string: str) -> tuple[list[str], bool]:
        """
        Simula la máquina de Turing con la cadena de entrada dada.
        Los movimientos son: R (derecha), L (izquierda). Los demás serán ignorados.
        :param input_string: Cadena de entrada
        :return: Una tupla con la lista de pasos de la simulación y un booleano que indica si la cadena fue aceptada
        """
        self.reset_tape(input_string)  # Reiniciar la cinta con la cadena de entrada y el símbolo en blanco
        current_state = self.initial_state  # Estado actual
        tape_position = 0  # Posición de la cinta
        derivation_process = []  # Lista de pasos de la simulación
        
        first_step = f"State: {current_state}, Tape: {''.join(self.tape)}, Head Position: {tape_position}"
        derivation_process.append(first_step)

        while current_state not in self.final_states and tape_position < len(self.tape):
            # Obtención del símbolo actual y la acción a realizar
            current_symbol = self.tape[tape_position]
            action = self.transitions[current_state][current_symbol]

            # Actualizar el símbolo en la cinta y el estado actual
            self.tape[tape_position] = action[1]  
            current_state = action[0]

            if(current_symbol == self.blank_symbol):
                self.tape.append(self.blank_symbol)

            # Actualizar la posición de la cinta
            if action[2] == "R": ## Si la acción es R, la cinta se mueve a la derecha
                tape_position += 1
            elif action[2] == "L":
                tape_position -= 1


            # Agregar el paso actual a la lista de pasos de la simulación
            tape_view = ''.join(self.tape)
            step_info = f"State: {current_state}, Tape: {tape_view}, Head Position: {tape_position}"
            derivation_process.append(step_info)

        is_accepted = current_state in self.final_states  # La cadena es aceptada si el estado actual es fina   l
        return derivation_process, is_accepted


def getMillionTest(turingMachine):
    print( "Probando un millon de veces")
    tiempos = {}
    input_string = "1"  
    while len(input_string) <= 20:
        print(f"n={len(input_string)}")
        start = time.time()
        turingMachine.simulate(input_string)
        end = time.time()
        tiempos[len(input_string)]= end - start
        
        with open('tiemposDeEjecucion.json', 'w') as json_file:
            json.dump(tiempos, json_file, indent=4)
        
        input_string +="1" 
    print("Terminado")
    
def plot_execution_times():
    # Lee los tiempos de ejecución del archivo JSON
    with open('tiemposDeEjecucion.json', 'r') as file:
        execution_times = json.load(file)

    # Prepara los datos para la gráfica
    lengths = list(execution_times.keys())
    times = [execution_times[key] for key in lengths]

    # Graficando
    plt.figure(figsize=(10, 6))
    plt.plot(lengths, times, marker='o', linestyle='-')
    plt.title('Tamaño de la cadena de entrada vs Tiempo de ejecución')
    plt.xlabel('Longitud de la cadena de entrada')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.grid(True)
    plt.savefig("plotExecutionTimes.png")
    plt.show()


if __name__ == "__main__":
    # TEST
    with open("backend/turing.json") as config_file:
        config = json.load(config_file)

    turing_machine = TuringMachine(**config)  # Leer el archivo json y crear una instancia de la máquina de Turing
    plot_execution_times()

    if input("Desea realizar prueba del millon?(Si, No) ") == "Si":
        getMillionTest(turing_machine)
    else:
        print("Expresion: 111")
        input_string = "111"
        while len(input_string) < 10:
            simulation_result, was_accepted = turing_machine.simulate(input_string)

        print(was_accepted)
        for step in simulation_result:
            print(step)
    
    plot_execution_times()
