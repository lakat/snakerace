import os
import tempfile
import shutil


class SampleTournament(object):
    def setup(self):
        self.temp_dir = tempfile.mkdtemp()
        self.lockdir = os.path.join(self.temp_dir, 'lockdir')
        return (
            'racer.py {lockdir}'.format(lockdir=self.lockdir),
            ['python', 'racer.py', self.lockdir]
        )

    def cleanup(self):
        if os.path.exists(self.lockdir):
            shutil.rmtree(self.lockdir)

    def teardown(self):
        shutil.rmtree(self.temp_dir)

