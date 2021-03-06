# coding=UTF-8
#
# Copyright (C) 2015  Michell Stuttgart

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import zipfile

from loader import Loader
from utility import Utility


class ZipLoader(Loader):
    def __init__(self, extension):
        super(ZipLoader, self).__init__(extension)

    def load(self, file_name):

        if not zipfile.is_zipfile(file_name) or not isinstance(file_name, str):
            return False

        try:
            zf = zipfile.ZipFile(file_name, 'r')
        except zipfile.BadZipfile, err:
            print '%20s  %s' % (file_name, err)
            return False
        except zipfile.LargeZipFile, err:
            print '%20s  %s' % (file_name, err)
            return False

        self._clear_data()
        name_list = zf.namelist()
        name_list.sort()

        list_size = len(name_list)
        count = 1

        for info in name_list:
            file_extension = Utility.get_file_extension(info)

            if not Utility.is_dir(info) and file_extension.lower() in \
                    self.extension:
                self.data.append({'data': zf.read(info), 'name': info})
                self.progress.emit(count * 100 / list_size)

            count += 1

        self.done.emit()
        zf.close()
        return True
