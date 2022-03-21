from multiprocessing import Pool
from blogapp import create_app, config, init_db, db as _db

# multiprocessing.set_start_method('spawn')  # Needed in Python 3.8 and later
# ctx = multiprocessing.get_context('spawn')
_pool = Pool(processes=12)
try:
    app = create_app(config_class_name=config.TestingConfig)
    app.run(use_reloader=True)
except KeyboardInterrupt:
    _pool.close()
# process = multiprocessing.Process(target=app.run, args=())
# process.start()