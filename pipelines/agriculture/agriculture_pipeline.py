from pipelines.agriculture.source import ofb
from pipelines.run import run_pipeline

if __name__ == "__main__":
    run_pipeline("agriculture", ofb())
