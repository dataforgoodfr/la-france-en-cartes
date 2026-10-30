from pipelines.run import run_pipeline
from pipelines.transverse.source import transverse

if __name__ == "__main__":
    run_pipeline("transverse", transverse())
