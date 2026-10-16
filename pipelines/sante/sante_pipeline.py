from pipelines.run import run_pipeline
from pipelines.sante.source import drees

if __name__ == "__main__":
    run_pipeline("sante", drees())
