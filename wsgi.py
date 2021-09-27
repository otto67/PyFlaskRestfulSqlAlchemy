
from app.__init__ import create_app
from app.app import create_tables

app = create_app()
create_tables()

if __name__ == "__main__":
  app.run()