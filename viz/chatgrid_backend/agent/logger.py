import sys
import logging

def default_server_logging(logger_name = 'server',
                          level=logging.DEBUG):
  """
  Enable or disable logging for a specific logger.

  Parameters
  ----------
  logger_name : str, optional
      Name of the logger to configure. 
      Default: "server"
  enable : bool, optional
      If True, enable the logger; if False, disable it.
  level : int, optional
      Logging level to set when enabling the logger.
      Common levels include:
      - logging.DEBUG     10
      - logging.INFO      20
      - logging.WARNING   30
      - logging.ERROR     40
      - logging.CRITICAL  50
      Default: logging.DEBUG
    Returns
    -------
      None
    """
  logger = logging.getLogger(logger_name)
  
  # Only add handler if none exists
  if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
  
  logger.setLevel(level)
  # Don't propagate to parent loggers (prevents duplicate logs from LangGraph)
  logger.propagate = False
  return logger