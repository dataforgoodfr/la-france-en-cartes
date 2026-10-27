from pipelines.securite.source import securite
from pipelines.run import run_pipeline

if __name__ == "__main__":
    run_pipeline("securite", securite())