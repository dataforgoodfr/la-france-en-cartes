from pipelines.education.source import education
from pipelines.run import run_pipeline

if __name__ == "__main__":
    run_pipeline("education", education())
