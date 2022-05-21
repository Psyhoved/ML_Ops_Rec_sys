Getting started
===============

This is where you describe how to get set up on a clean install, including the
commands necessary to get the raw data (using the `sync_data_from_s3` command,
for example), and then how to make the cleaned, final data sets.


1. После установки библиотеки streamlit нужно поправить в файле
env/Lib/site-packages/streamlit/watcher/local_sources_watcher.py
строку 83:
 # for wm in self._watched_modules.values():
 #      if wm.module_name is not None and wm.module_name in sys.modules:
 #           del sys.modules[wm.module_name]

на

 # for wm in self._watched_modules.values():
 #      if wm.module_name is not None and wm.module_name in sys.modules:
 #          pass
 #           # del sys.modules[wm.module_name]
Библиотека streamlit удаляет из библиотеки sys модули. Второй вариант, чтобы все корректно работало:

Добавить в модули, использующие библиотеку streamlit следующий код:
# import warnings
# warnings.filterwarnings('ignore')