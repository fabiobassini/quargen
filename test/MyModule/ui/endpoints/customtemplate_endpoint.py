from flask import render_template
from utils.logger import ColoredLogger
logger = ColoredLogger(__name__).get_logger()

def register_endpoint(parent_bp):
    @parent_bp.route('/custom')
    def customtemplate_view():
        logger.info("Richiesta per CustomTemplate endpoint")
        return render_template('customtemplate/customtemplate.html')
