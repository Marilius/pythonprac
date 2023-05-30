from doit.task import clean_targets
import shutil


DOIT_CONFIG = {'default_tasks': ['html']}


def task_i18n():
    """Compile translations"""
    return {
        'actions': ['pybabel compile -d moodserver/moodserver/translation -D moodserver'],
        'file_dep': ['moodserver/moodserver/translation/ru/LC_MESSAGES/moodserver.po'],
        'targets': ['moodserver/moodserver/translation/ru/LC_MESSAGES/moodserver.mo'],
        # 'clean': True,
    }


def task_extract():
    """Extract translations"""
    return {
        'actions': ['pybabel extract --input-dirs moodserver/moodserver -o moodserver/moodserver/moodserver.pot'],
        'targets': ['moodserver/moodserver/moodserver.pot'],
        'clean': True,
    }


def task_update():
    """Update translations"""
    return {
        'actions': ['pybabel update -D moodserver -d moodserver/moodserver/translation -i moodserver/moodserver/moodserver.pot'],
        'file_dep': ['moodserver/moodserver/moodserver.pot'],
        'targets': ['moodserver/moodserver/translation/ru/LC_MESSAGES/moodserver.po'],
        'clean': True,
    }


def task_test():
    """Test MOOD"""
    return {
        'actions': ['python -m unittest -v'],
        'file_dep': ['test_server.py'],
        'task_dep': ['i18n'],
        # 'clean': True,
    }


def task_html():
    """Build html documentation"""
    return {
        'actions': ['sphinx-build docs/source docs/build'],
        'task_dep': ['i18n'],
        'targets': ['docs/build'],
        'clean': [clean_targets, lambda: shutil.rmtree('docs/build')]
    }


def task_whlserver():
    """Make server wheel"""
    return {
        'actions': ['python3 -m build -n -w moodserver'],
        'task_dep': ['i18n'],
        'file_dep': ['moodserver/pyproject.toml', 'moodserver/moodserver/translation/ru/LC_MESSAGES/moodserver.mo'],
        'targets': ['moodserver/dist/*.whl'],
        'clean': [lambda: shutil.rmtree('moodserver/dist'), lambda: shutil.rmtree('moodserver/build'), lambda: shutil.rmtree('moodserver/MoodServer.egg-info')],
    }


def task_whlclient():
    """Make client wheel"""
    return {
        'actions': ['python3 -m build -n -w moodclient'],
        'file_dep': ['moodclient/pyproject.toml'],
        'targets': ['moodclient/dist/*.whl'],
        'clean': [lambda: shutil.rmtree('moodclient/dist'), lambda: shutil.rmtree('moodclient/build'), lambda: shutil.rmtree('moodclient/MoodClient.egg-info')],
    }


def task_w():
    """Make wheels"""
    return {
        'actions': None,
        'task_dep': ['whlserver', 'whlclient'],
        'clean': [
            lambda: shutil.rmtree('moodclient/dist'), lambda: shutil.rmtree('moodclient/build'), lambda: shutil.rmtree('moodclient/MoodClient.egg-info'),
            lambda: shutil.rmtree('moodserver/dist'), lambda: shutil.rmtree('moodserver/build'), lambda: shutil.rmtree('moodserver/MoodServer.egg-info'),
        ],
    }
