'''
NATALIA OSEJO HINCAPIE 
PATRÓN DE DISEÑO OBSERVER
'''

from datetime import datetime, timedelta 

# Definimos la interfaz para los suscriptores 
class IReminderSubscriber: 
    def update_reminder(self, task): 
        pass 

# Definimos el notificador de recordatorios 
class ReminderNotifier: 
    def __init__(self) -> None: 
        self._subscribers = [] 

    def attach(self, subscriber: IReminderSubscriber): 
        if subscriber not in self._subscribers: 
            self._subscribers.append(subscriber) 

    def detach(self, subscriber: IReminderSubscriber): 
        if subscriber in self._subscribers: 
            self._subscribers.remove(subscriber) 

    def notify(self, task): 
        for subscriber in self._subscribers: 
            subscriber.update_reminder(task) 

# Creamos un suscriptor concreto para los recordatorios 
class TaskReminderSubscriber(IReminderSubscriber): 
    def update_reminder(self, task): 
        if task.due_date and (task.due_date - datetime.now()) < timedelta(days=7): 
            print(f"¡Recordatorio! La tarea '{task.title}' ({task.description}) está próxima a su fecha de vencimiento el {task.due_date}.") 

# Definimos la clase de tarea 
class Task: 
    def __init__(self, title, description, due_date=None) -> None: 
        self.title = title 
        self.description = description  # Agregamos la descripción
        self.due_date = due_date 
        self.completed = False 

# Clase principal para el Gestor de Tareas 
class TaskManager: 
    def __init__(self) -> None: 
        self.tasks = [] 
        self.completed_tasks = [] 
        self.reminder_notifier = ReminderNotifier() 

    def add_task(self, task): #añadir tarea
        self.tasks.append(task) 
        if task.due_date: 
            self.reminder_notifier.notify(task) 

    def mark_task_as_completed(self, task): #marcar como completada
        if task in self.tasks: 
            self.tasks.remove(task) 
            task.completed = True 
            self.completed_tasks.append(task) 

    def get_pending_tasks(self): #retornar tareas pendientes
        return self.tasks 

    def get_completed_tasks(self): #retornar tareas completadas
        return self.completed_tasks 

    def get_reminders(self): #retornar recordatorios
        # Ordenar las tareas por fecha de vencimiento
        return sorted(self.tasks, key=lambda x: x.due_date if x.due_date else datetime.max)

def print_tasks_with_description(tasks): #imprimir tareas junto a su descripcion
    print("Lista de tareas:") 
    for i, task in enumerate(tasks, 1): 
        print(f"{i}. {task.title}: {task.description}") 
        if task.due_date: 
            print(f"   Fecha de vencimiento: {task.due_date}") 
        else: 
            print("   Sin fecha de vencimiento") 
        print("") 

def print_reminders(reminders): #imprimir recordatorios
    print("\n------ Recordatorios ------") 
    if reminders: 
        for reminder in reminders: 
            if reminder.due_date and (reminder.due_date - datetime.now()) < timedelta(days=7): 
                print(f"¡Recordatorio! La tarea '{reminder.title}' ({reminder.description}) está próxima a su fecha de vencimiento el {reminder.due_date}.") 
    else: 
        print("No hay recordatorios próximos.") 
    print("--------------------------") 



#--------------------- programa consola
if __name__ == '__main__':
    task_manager = TaskManager()

    # Agregar algunas tareas de prueba
    task_manager.add_task(Task("Hacer la compra", "Comprar alimentos para la semana", datetime.now() + timedelta(days=1)))
    task_manager.add_task(Task("Llamar al médico", "Hacer cita para chequeo anual", datetime.now() + timedelta(days=8)))
    task_manager.add_task(Task("Preparar informe", "Terminar informe mensual para el trabajo", datetime.now() + timedelta(days=5)))
    task_manager.add_task(Task("Ir al gimnasio", "Entrenamiento de fuerza y cardio", datetime.now() + timedelta(days=40, hours=12)))

    # Creamos los suscriptores y los adjuntamos al notificador de recordatorios
    task_reminder_subscriber = TaskReminderSubscriber()
    task_manager.reminder_notifier.attach(task_reminder_subscriber)

    while True:
        # Mostrar recordatorios antes de mostrar el menú principal
        reminders = task_manager.get_reminders()
        print_reminders(reminders)

        print("\n------ MENÚ ------")
        print("1. Añadir tarea")
        print("2. Ver tareas pendientes y completadas")
        print("3. Marcar tarea como completada")
        print("4. Salir")

        choice = input("Ingrese el número correspondiente a la opción que desea realizar: ")

        if choice == '1':
            while True:
                title = input("Ingrese el título de la tarea: ")
                description = input("Ingrese la descripción de la tarea: ")
                while True:
                    due_date_input = input("Ingrese la fecha de vencimiento (opcional - dejar en blanco para omitir en el formato 'AAAA-MM-DD HH:MM'): ")

                    if due_date_input:
                        try:
                            due_date = datetime.strptime(due_date_input, "%Y-%m-%d %H:%M")
                        except ValueError:
                            try:
                                # Interpretar la entrada como fecha sin hora
                                due_date = datetime.strptime(due_date_input, "%Y-%m-%d")
                                # Establecer la hora predeterminada a las 00:00
                                due_date = due_date.replace(hour=0, minute=0)
                            except ValueError:
                                print("Formato de fecha no válido. Por favor, ingrese en el formato 'AAAA-MM-DD HH:MM'")
                                continue
                        break  # Salir del bucle si la fecha es válida
                    else:
                        due_date = None  # Definir una fecha de vencimiento predeterminada si no se proporciona una fecha
                        break  # Salir del bucle si no se proporciona una fecha

                # Crear la tarea y añadirla al gestor de tareas
                task = Task(title, description, due_date)
                task_manager.add_task(task)

                add_another = input("¿Quiere añadir otra tarea? (s/n): ")
                if add_another.lower() != 's':
                    break

        elif choice == '2':
            while True:
                try:
                    print("\n------ Ver Tareas ------")
                    print("\nTareas pendientes:")
                    print_tasks_with_description(task_manager.get_pending_tasks())

                    print("\nTareas completadas:")
                    print_tasks_with_description(task_manager.get_completed_tasks())
                    view_choice = input("\nIngrese 0 para volver al menú anterior: ")

                    if view_choice == '0':
                        break
                    else:
                        print("Opción no válida. Por favor, ingrese un número válido.")
                except ValueError:
                    print("Opción no válida. Por favor, ingrese un número válido.")
        
        elif choice == '3':
            while True:
                try:
                    print("\nTareas pendientes:")
                    pending_tasks = task_manager.get_pending_tasks()
                    for i, task in enumerate(pending_tasks, 1):
                        print(f"{i}. {task.title}: {task.description}")
                        if task.due_date:
                            print(f"   Fecha de vencimiento: {task.due_date}")
                        else:
                            print("   Sin fecha de vencimiento")
                        print("")

                    task_index = int(input("Ingrese el número de la tarea que desea marcar como completada: ")) - 1
                    task_to_complete = pending_tasks[task_index]
                    task_manager.mark_task_as_completed(task_to_complete)

                    print("\nTarea marcada como completada.")

                    while True:
                        complete_another = input("¿Desea completar otra tarea? (s/n): ")
                        if complete_another.lower() == 's' or complete_another.lower() == 'n':
                            break
                        else:
                            print("Opción no válida. Por favor, ingrese 's' para sí o 'n' para no.")

                    if complete_another.lower() != 's':
                        break
                except (ValueError, IndexError):
                    print("Opción no válida. Por favor, ingrese un número válido.")

        elif choice == '4':
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, ingrese un número válido.") 