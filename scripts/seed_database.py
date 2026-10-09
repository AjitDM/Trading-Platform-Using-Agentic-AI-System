from src.persistence.database import initialize_database


def main() -> None:
    initialize_database()
    print("Database tables created.")


if __name__ == "__main__":
    main()