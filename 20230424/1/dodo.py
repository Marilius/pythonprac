from doit.task import clean_targets
import shutil


DOIT_CONFIG = {'default_tasks': ['html']}


def task_compile():
    """Compile translations"""
    return {
            'actions': ['pybabel compile -D server -d moodserver/translation'],
            'file_dep': ['moodserver/translation/ru/LC_MESSAGES/server.po'],
            'targets': ['moodserver/translation/ru/LC_MESSAGES/server.mo'],
            'clean': True,
           }


def task_extract():
    """Extract translations"""
    return {
            'actions': ['pybabel extract -o moodserver/server.pot --input-dirs moodserver/'],
            'targets': ['moodserver/server.pot']
           }


def task_update():
    """Update translations"""
    return {
            'actions': ['pybabel update -D server -d moodserver/translation -i moodserver/server.pot'],
            'file_dep': ['moodserver/server.pot'],
            'targets': ['moodserver/translation/ru/LC_MESSAGES/server.po'],
           }


def task_test():
    """Test MOOD"""
    return {
            'actions': ['python -m unittest -v'],
            'file_dep': ['test_server.py'],
            'task_dep': ['compile'],
            'clean': True,
           }


def task_html():
    """Build html documentation"""
    return {
            'actions': ['sphinx-build docs/source docs/build'],
            'task_dep': ['compile'],
            'targets': ['docs/build'],
            'clean': [clean_targets, lambda: shutil.rmtree('docs/build')]
            }


def task_server():
    """Make server wheel"""
    return {
        'actions': ['python -m build -n -w moodserver'],
        'task_dep': ['compile'],
        'file_dep': ['moodserver/pyproject.toml', 'moodserver/translation/ru/LC_MESSAGES/server.mo'],
        'targets': ['moodserver/dist/*.whl'],
        'clean': [lambda: shutil.rmtree('moodserver/dist'), lambda: shutil.rmtree('moodserver/build'), lambda: shutil.rmtree('moodserver/MoodServer.egg-info')],
        }


def task_client():
    """Make client wheel"""
    return {
        'actions': ['python -m build -n -w moodclient'],
        'file_dep': ['moodclient/pyproject.toml'],
        'targets': ['moodclient/dist/*.whl'],
        'clean': [lambda: shutil.rmtree('moodclient/dist'), lambda: shutil.rmtree('moodclient/build'), lambda: shutil.rmtree('moodclient/MoodClient.egg-info')],
        }


def task_w():
    """Make wheels"""
    return {
        'actions': None,
        'task_dep': ['server', 'client'],
        }
