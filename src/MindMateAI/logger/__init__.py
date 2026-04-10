import logging
import sys
import os


def get_logger(name: str = "MindMateAI Logger") -> logging.Logger:
    """
    Returns a logger that works safely on Windows (cp1252) by replacing
    unicode characters with ASCII-safe equivalents before emitting.
    """

    class SafeStreamHandler(logging.StreamHandler):
        """StreamHandler that replaces unencodable characters instead of crashing."""

        def emit(self, record):
            try:
                msg = self.format(record)
                stream = self.stream
                # Replace common unicode symbols that break cp1252 on Windows
                msg = (
                    msg
                    .replace('\u2192', '->')    # -> (right arrow)
                    .replace('\u2190', '<-')    # <- (left arrow)
                    .replace('\u2714', '[OK]')  # checkmark
                    .replace('\u2718', '[X]')   # cross mark
                    .replace('\u2014', '--')    # em dash
                    .replace('\u2013', '-')     # en dash
                    .replace('\u2022', '*')     # bullet
                    .replace('\u25ba', '>')     # filled right arrow
                    .replace('\u2640', '')
                    .replace('\u2642', '')
                )
                # Final fallback: encode/decode with replacement for any remaining chars
                if hasattr(stream, 'encoding') and stream.encoding:
                    msg = msg.encode(stream.encoding, errors='replace').decode(stream.encoding)
                stream.write(msg + self.terminator)
                self.flush()
            except Exception:
                self.handleError(record)

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Console handler with safe encoding
        handler = SafeStreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="[%(asctime)s - %(name)s - %(levelname)s - %(message)s]",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # File handler — always UTF-8, no encoding issues
        try:
            log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            file_handler = logging.FileHandler(
                os.path.join(log_dir, 'mindmate.log'),
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            pass  # If log file can't be created, console logging still works

        logger.propagate = False

    return logger


# Single shared logger instance
logger = get_logger("MindMateAI Logger")