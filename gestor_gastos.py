from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

ARCHIVO = "gastos.csv"

def inicializar_archivo():
    try:
        pd.read_csv(ARCHIVO)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "category", "description", "amount"])
        df.to_csv(ARCHIVO, index=False)

def agregar_gasto(fecha, categoria, descripcion, monto):
    df = pd.read_csv(ARCHIVO)
    nuevo = {"date": fecha, "category": categoria, "description": descripcion, "amount": monto}
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(ARCHIVO, index=False)
    print("✅ Expense added successfully.")

def resumen():
    df = pd.read_csv(ARCHIVO)
    print("\n📊 Expense summary:")
    print(df.groupby("category")["amount"].sum())
    print(f"\n💰 Total expense: {df['amount'].sum()}")

def graficar():
    df = pd.read_csv(ARCHIVO)
    df.groupby("category")["amount"].sum().plot(kind="bar")
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.show()

def menu():
    inicializar_archivo()
    while True:
        print("\n--- Expense Manager ---")
        print("1. Add expense")
        print("2. View summary")
        print("3. Plot expenses")
        print("4. Exit")
        opcion = input("Choose an option: ")

        if opcion == "1":
            fecha_input = input("Date (YYYY-MM-DD) [Enter for today]: ")
            if fecha_input.strip() == "":
                fecha = datetime.today().strftime("%Y-%m-%d")
            else:
                try:
                    fecha = datetime.strptime(fecha_input, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    print("⚠️ Invalid format. Using today's date instead.")
                    fecha = datetime.today().strftime("%Y-%m-%d")

            categoria = input("Category: ")
            descripcion = input("Description: ")
            monto = float(input("Amount: "))
            agregar_gasto(fecha, categoria, descripcion, monto)

        elif opcion == "2":
            resumen()

        elif opcion == "3":
            graficar()

        elif opcion == "4":
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    menu()
