import os
import subprocess
import sublime
import sublime_plugin


def get_setting(key):
  settings = sublime.load_settings("FormatX.sublime-settings")
  return settings.get(key)

def get_command(scope):
  langs = get_setting("scope")

  if isinstance(langs, dict):
    return langs.get(scope)

  return None

# cmd: command arrya, e.g. ['goimports']
def run_cmd(_cmd, stdin, path):
  def replace(part):
    if part == "$file":
      return path

    # replace `~`
    return os.path.expanduser(part)

  cmd = [replace(part) for part in _cmd]

  proc = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdout=subprocess.PIPE,
  )

  if isinstance(stdin, str):
    stdin = stdin.encode("utf8")

  stdout, stderr = proc.communicate(stdin)
  return stdout, stderr, proc.returncode

def format(view, edit):
  scope = view.syntax().scope
  cmd = get_command(scope)

  if not cmd:
    return

  region = sublime.Region(0, view.size())
  code = view.substr(region)
  stdout, stderr, code = run_cmd(cmd, code, view.file_name())

  if code != 0:
    msg = ""
    try:
      stdoutstr = stdout.decode("utf8").strip()
      if stdoutstr != "":
        msg = stdoutstr.split("\n")[0]
      else:
        stderrstr = stderr.decode("utf8").strip()
        msg = stderrstr.split("\n")[0]
    except:
      msg = "failed to format"

    view.window().status_message("FormatX: %s" % msg)
    return

  try:
    stdoutstr = stdout.decode("utf8")
    view.replace(edit, region, stdout.decode("utf8"))
  except:
    view.window().status_message("FormatX: output is not valid utf8")

class FormatxFormat(sublime_plugin.TextCommand):
  def is_enabled(self):
    scope = self.view.syntax().scope
    cmd = get_command(scope)
    return cmd is not None

  def run(self, edit):
    format(self.view, edit)

class FormatxListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
      name = view.file_name()

      if name is None:
        return

      dirs = [os.path.expanduser(dir) for dir in (get_setting("auto_format_dirs") or [])]

      if any([name.startswith(dir) for dir in dirs]):
        view.run_command('formatx_format')
