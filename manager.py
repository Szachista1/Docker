import os
import time
import sys

# --- KONFIGURACJA PRODUKCYJNA ---
# W Dockerze używamy nazw usług jako hostów
MASTER_HOST = "mysql_master"
SLAVE_HOST = "mysql_slave"

# Te dane muszą pasować do tych w pliku .env
DB_USER = "wordpress_user"
DB_PASS = "TrudneHasloUsera!"  # Upewnij się, że to hasło jest takie samo jak w .env!
DB_NAME = "wordpress_db"

def menu():
    while True:
        print("\n--- PANEL ZARZĄDZANIA PRODUKCJĄ (CLOUD) ---")
        print("1. Kopia zapasowa (Backup) z MASTERA")
        print("2. Przywracanie danych na SLAVE (Synchronizacja)")
        print("3. Sprawdź status baz danych (Ping)")
        print("4. Wyjście")
        
        choice = input("Wybierz opcję: ")

        if choice == "1":
            print("Tworzenie backupu z Mastera...")
            # Używamy flagi -h z nazwą usługi
            cmd = f"mysqldump -h {MASTER_HOST} -u {DB_USER} -p{DB_PASS} --skip-ssl --no-tablespaces {DB_NAME} > backup.sql"
            os.system(cmd)
            print("Backup zapisany w kontenerze jako backup.sql")

        elif choice == "2":
            print("Wgrywanie danych na Slave...")
            # Slave domyślnie jest read-only, ale root może to ominąć przy imporcie
            cmd = f"mysql -h {SLAVE_HOST} -u root -pTrudneHasloRoota! --skip-ssl {DB_NAME} < backup.sql"
            os.system(cmd)
            print("Dane zsynchronizowane na Slave.")

        elif choice == "3":
            print("\n--- STATUS POŁĄCZEŃ ---")
            print(f"Sprawdzanie Mastera ({MASTER_HOST})...")
            os.system(f"mysqladmin -h {MASTER_HOST} -u {DB_USER} -p{DB_PASS} --skip-ssl ping")
            
            print(f"Sprawdzanie Slave'a ({SLAVE_HOST})...")
            os.system(f"mysqladmin -h {SLAVE_HOST} -u root -pTrudneHasloRoota! --skip-ssl ping")

        elif choice == "4":
            print("Zamykanie panelu.")
            sys.exit()

        else:
            print("Niepoprawny wybór.")

if __name__ == "__main__":
    # Czekamy chwilę na start bazy po uruchomieniu kontenera
    print("Czekam 10 sekund na start usług...")
    time.sleep(10)
    menu()