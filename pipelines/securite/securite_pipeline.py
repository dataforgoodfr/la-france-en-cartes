from pipelines.run import run_pipeline
from pipelines.securite.source import securite

if __name__ == "__main__":
    run_pipeline("securite", securite())
