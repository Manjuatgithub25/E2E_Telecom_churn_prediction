import os, datetime, logging, sys

# script_name = os.path.splitext(os.path.basename(__file__))[0]
logger_format = "[%(asctime)s] - %(lineno)d - %(levelname)s - %(filename)s - %(message)s"
log_dir = "Logs"
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_path = os.path.join(log_dir, f"running_logs_{current_time}.log")

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logger_format,
    handlers=[
        logging.FileHandler(file_path),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
