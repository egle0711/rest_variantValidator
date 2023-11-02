import json
from representations.bin.siren_object_api_impl import SirenObjectAPI
from representations.libs.exceptions import SirenDumpException

__author__ = 'atomikin'


class JSON(SirenObjectAPI):

    def dump(self, indent=None):
        params = self._dict
        res = self.check_input(params)
        if sum(res) == len(res):
            return json.dumps(self._dict, indent=indent)
        err_msg = 'Provided keys "{}", while should be in "{}", where "{}" are required.'.format(
            params.keys(),
            self.LIMITED,
            self.REQUIRED
        )
        raise SirenDumpException(err_msg)

    def load(self, data: str):
        """
        TMP version. Won't work with Representations.
        :param data:
        :return:
        """
        self.append(json.loads(data))
        return self


