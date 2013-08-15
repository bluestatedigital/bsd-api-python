import logging

class Factory:
    logMap = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'critical': logging.CRITICAL
    }

    def create( self, level ):
        try:
            llevel = self.logMap[level.lower()]
        except KeyError:
            llevel = logging.WARNING

        logger = logging.getLogger('pageload')
        logger.setLevel(llevel)
        ch = logging.StreamHandler()
        ch.setLevel(llevel)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
