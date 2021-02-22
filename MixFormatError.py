import re

SYNTAX_ERROR_RE = re.compile(
    r"^\*\*\s\((.+)\)\s([^:]+):(\d+)(?::\d+)?:\s(.+)$",
    re.MULTILINE | re.IGNORECASE | re.UNICODE)

# ** (Mix) Unknown dependency :assertions given to :import_deps in the formatter configuration. The dependency is not listed in your mix.exs for environment :dev
DEPENDENCY_ERROR_RE = re.compile(
    r"^\*\*\s\((.+)\)\sUnknown dependency\s(.+)\sin the formatter configuration.+environment\s(:.+)$",
    re.MULTILINE | re.IGNORECASE | re.UNICODE)

class MixFormatError:
    def __init__(self, stdout, stderr):
        self.__stdout = stdout
        self.__stderr = stderr
        self.__deps_matches = DEPENDENCY_ERROR_RE.search(stdout)
        self.__syntax_matches = SYNTAX_ERROR_RE.search(stdout + stderr)

    @property
    def stdout(self):
        return self.__stdout

    @property
    def stderr(self):
        return self.__stderr

    @property
    def full_message(self):
        if self.__syntax_matches:
            return self.__syntax_matches.group(0)
        elif self.__deps_matches:
            return self.__deps_matches.group(0)
        else:
            return "stdout: {0}\nstderr: {1}".format(self.stdout, self.stderr)

    @property
    def line(self):
        if self.__syntax_matches:
            return int(self.__syntax_matches.group(3))
        else:
            return None

    @property
    def status_message(self):
        if self.__syntax_matches:
            return "{0} - {1}".format(self.__syntax_matches.group(1), self.__syntax_matches.group(4))
        elif self.__deps_matches:
            return "unknown dependency: {0} for env {1}".format(self.__deps_matches.group(2), self.__deps_matches.group(3))
        else:
            "unknown error - check console for details"

    @property
    def did_match(self):
        return self.__syntax_matches is not None or self.__deps_matches is not None
