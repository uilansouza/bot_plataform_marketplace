import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
import signal
import psutil




#print("pids",os.system('ps -a'))

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        output = os.popen('ps -a').read().split('\n')
        if event.is_directory:
            return None
        elif event.event_type == 'modified' and event.src_path.endswith('.py'):
            print('Arquivo modificado: {}'.format(event.src_path))
            for line in output:
                # Verifica se o processo contém a string "python"
                if "python"  in line:
                    # Obtém o ID do processo
                    pid = line.split()[0]
                    if os.getpid() != pid:
                        print(f"pid atual {os.getpid()}")
                        os.system(f'kill {pid}')

                    # Mata o processo pelo seu ID
                    os.system(f'kill {pid}')
                    filename = "main2.py"
                    dir_path = os.path.dirname(os.path.abspath(__file__))
                    filepath = os.path.join(dir_path, filename)
                    print(filepath)
                    # os.system(f'python {filepath}')

             # Aqui você pode colocar o código que reinicia o script
            # Por exemplo, chamar uma função que encerra o processo atual e inicia um novo

if __name__ == "__main__":
    path = './src' # Diretório que será monitorado
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
