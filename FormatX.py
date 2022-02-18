import os
import subprocess
import sublime
import sublime_plugin

settings = sublime.load_settings("FormatX.sublime-settings")

def get_command(scope):
  langs = settings.get("langs")

  if isinstance(langs, dict):
    return langs.get(scope)

  return None

# cmd: command arrya, e.g. ['goimports']
def run_cmd(_cmd, stdin):
  # replace `~`
  cmd = [os.path.expanduser(part) for part in _cmd]

  proc = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdout=subprocess.PIPE,
    cwd=os.path.expanduser("~/Desktop/Lab/yarn-lab"),
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
  stdout, stderr, code = run_cmd(cmd, code)

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

