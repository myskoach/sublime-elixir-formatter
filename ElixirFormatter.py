import os
import sublime
import sublime_plugin
import subprocess
import threading
import re

from .MixFormatError import MixFormatError

PLUGIN_NAME = "ElixirFormatter"
PLUGIN_CMD_NAME = "elixir_formatter_format_file"

class ElixirFormatter:
    @staticmethod
    def run(view, edit, file_name):
        project_root_with_mix = ElixirFormatter.find_project(file_name)
        project_root = project_root_with_mix or os.path.dirname(file_name)
        file_name_rel = file_name.replace(project_root + "/", "")

        blacklisted = ElixirFormatter.check_blacklisted_in_config(project_root, file_name_rel)
        if blacklisted:
            print("{0} skipped '{1}' due to :inputs key in '.formatter.exs'".
              format(PLUGIN_NAME, file_name_rel))
            return

        region = sublime.Region(0, view.size())
        [stdout, stderr, exit_code] = ElixirFormatter.run_command(project_root, ["mix", "format", file_name_rel])
        if exit_code == 0:
            previous_position = view.viewport_position()
            Utils.indent(view)
            Utils.restore_position(view, previous_position)
            Utils.st_status_message("file formatted")
        else:
            error = MixFormatError(stdout, stderr)

            if error.did_match:
                print("{0}: {1}".format(PLUGIN_NAME, error.full_message))
                Utils.st_status_message(error.status_message)
                if error.line is not None: view.run_command("goto_line", {"line": error.line})
            else:
                print("{0} stdout: {1}".format(PLUGIN_NAME, stdout))
                print("{0} stderr: {1}".format(PLUGIN_NAME, stderr))
                Utils.st_status_message("unknown error - check console for details")

    @staticmethod
    def find_project(cwd = None):
        cwd = cwd or os.getcwd()
        if cwd == os.path.realpath('/'):
            return None
        elif os.path.exists(os.path.join(cwd, 'mix.exs')):
            return cwd
        else:
            return ElixirFormatter.find_project(os.path.dirname(cwd))

    @staticmethod
    def run_command(project_root, task_args):
        settings = sublime.load_settings('Preferences.sublime-settings')
        env = os.environ.copy()

        env['MIX_ENV'] = 'test'

        try:
            env['PATH'] = os.pathsep.join([settings.get('env')['PATH'], env['PATH']])
        except (TypeError, ValueError, KeyError):
            pass

        if sublime.platform() == "windows":
            launcher = ['cmd', '/c']
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            launcher = []
            startupinfo = None

        process = subprocess.Popen(
            launcher + task_args,
            cwd = project_root,
            env = env,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            startupinfo = startupinfo)

        stdout, stderr = process.communicate()
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        exit_code = process.returncode

        return [stderr, stdout, exit_code]

    check_blacklisted_script_template = """
      file = \"[[file]]\"
      formatter = \".formatter.exs\"
      with true <- File.exists?(formatter),
           {formatter_opts, _} <- Code.eval_file(formatter),
           {:ok, inputs} <- Keyword.fetch(formatter_opts, :inputs) do
        IO.puts("Check result: #{file in Enum.flat_map(inputs, &Path.wildcard/1)}")
      end
    """

    @staticmethod
    def check_blacklisted_in_config(project_root, file_name):
        if not os.path.isfile(os.path.join(project_root, ".formatter.exs")):
            return

        script = ElixirFormatter.check_blacklisted_script_template.replace("[[file]]", file_name)
        [stderr, stdout, exit_code] = ElixirFormatter.run_command(project_root, ["elixir", "-e", script])
        return "Check result: false" in stdout

class ElixirFormatterFormatFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name = self.view.file_name()
        extension = os.path.splitext(file_name)[1][1:]
        syntax = self.view.settings().get("syntax")
        if extension in ["ex", "exs"] or "Elixir" in syntax:
            threading.Thread(target=ElixirFormatter.run, args=(self.view, edit, file_name,)).start()

class ElixirFormatterEventListeners(sublime_plugin.EventListener):
    @staticmethod
    def on_pre_save(view):
        view.run_command(PLUGIN_CMD_NAME)

class Utils:
    @staticmethod
    def trim_trailing_ws_and_lines(val):
        if val is None:
            return val
        val = re.sub(r'\s+\Z', '', val)
        return val

    @staticmethod
    def indent(view):
        view.run_command('detect_indentation')

    @staticmethod
    def restore_position(view, previous_position):
        view.set_viewport_position((0, 0), False)
        view.set_viewport_position(previous_position, False)

    @staticmethod
    def replace(view, edit, region, text):
        view.replace(edit, region, text)

    @staticmethod
    def st_status_message(msg):
        sublime.set_timeout(lambda: sublime.status_message('{0}: {1}'.format(PLUGIN_NAME, msg)), 0)
