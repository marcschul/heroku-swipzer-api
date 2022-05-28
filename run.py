from app.main import app
from app.init_db import init

def main():
  init()
  if __name__ == "__main__":
    app.run()

main()